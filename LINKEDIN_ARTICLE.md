# From a throwaway script to a Splunkbase app: what I learned building MISPFuse

*About a 9-minute read. The real version of how a 30-line script became a
published Splunk app, including the one compatibility problem that nearly
ended the whole thing.*

Most of the useful tools I've built started as something I wouldn't have shown
anyone. MISPFuse was no different.

The problem was boring. My team worked in Splunk. Our threat intel lived in
MISP. And the connection between the two, taking indicators we found in Splunk
and getting them into MISP as events and attributes, was me. Copying values by
hand. Slow, and easy to get wrong.

So I wrote a script. PyMISP, the official Python client, makes the MISP side
almost too easy: a PyMISP object, a MISPEvent, add_attribute, add_event, done.
The first version was maybe thirty lines. It had a keys.py with my MISP URL and
API key sitting there in plaintext, a hardcoded org id, TLS verification turned
off because my lab used a self-signed cert, and one big assumption baked in:
everything is an IP under "Network activity."

It worked on my laptop, for me. That was the whole scope, and for a while that
was fine.

## Getting it into Splunk

The trouble with a laptop script is that it stays on your laptop. Nobody else
could run it. But Splunk has an extension point that looked made for this: the
custom search command.

The idea is clean. You write a Python class, Splunk feeds it search results row
by row, and you do whatever you want with them. I turned my script into a
StreamingCommand. Now anyone could type `... | mispfuse` and their indicators
would land in MISP. The first time a colleague ran it, it felt like it had been
worth the afternoon.

Going from "a script for me" to "a command for the team" also put every
shortcut I'd taken on display. The org id was still hardcoded to my MISP org.
The API key was still in keys.py, now shipped inside the app where everyone
could read it. TLS was still off. And the command made one MISP event per row,
so pushing five hundred IPs got you five hundred separate events. That isn't how
anyone models threat intel.

The worst part was that IP assumption. Real indicators are IPs, domains, URLs,
hashes, email addresses. Dozens of MISP types, each valid only in certain
categories. My command forced one type and fell over on anything else.

It was a proof of concept wearing a product costume.

## Deciding to publish

Here's the thing about building something people find useful: they want it too.
I started getting asked whether they could install it on their Splunk and point
it at their MISP. The natural home for that is Splunkbase.

And that's where I hit a wall. The good kind, the kind that makes you fix things.

Splunkbase apps go through AppInspect, an automated check, and if you want to
run on Splunk Cloud there's a stricter cloud pass on top. The very first thing
that fails cloud vetting is a plaintext credential in a config file. My keys.py
was an instant no. So was my lib/ folder, which by then was a graveyard. I'd
pip installed into it so many times it had three versions of urllib3, two of
PyMISP, and a whole virtual environment committed by accident. The app had even
nested inside itself somehow.

Two options. Hand-roll a real setup page with encrypted credential storage,
REST handlers, input validation, and a clean dependency install, which is weeks
of fiddly plumbing that's easy to get subtly wrong. Or find something that
already did it.

## UCC

UCC, the Universal Configuration Console, is Splunk's own answer to exactly
this. It's a pip package (splunk-add-on-ucc-framework). You describe your app's
configuration in one JSON file, globalConfig.json, and it generates the parts
nobody enjoys writing: the React config UI, the REST handlers behind it,
encrypted credential storage in storage/passwords, proxy and logging tabs, and
(this part surprised me) scaffolding for alert actions and custom search
commands too.

The model clicked fast. In globalConfig.json I declared an Account tab, so
people add their own MISP instances through the UI with the key encrypted for
them. No more keys.py. Proxy and logging tabs came basically for free. An alert
action, so indicators could go out on a schedule. And a search command,
mispfusepush, for ad-hoc pushes.

Then you run three commands, init, build, package, and out comes a clean app.
The dependency mess solved itself: UCC installs from a requirements.txt into a
fresh lib/, and an exclude.txt strips anything Splunk already ships so you don't
end up with duplicates. The exact thing that had bloated my old build to 26 MB
just couldn't happen anymore.

It felt like someone had taken the twenty boring jobs between me and a
publishable app and quietly done nineteen of them.

## The problem that nearly sank it

Then I hit the one I couldn't design around.

I wanted the latest PyMISP, the 2.5 line that keeps up with current MISP
servers. But PyMISP has required Python 3.10 or newer since January 2024. And
Splunk ships its own Python for running commands and alert actions. On Splunk
9.x, and even 10.0 and 10.1, that Python is 3.9.

3.9 is older than PyMISP needs. So the newest PyMISP won't even import on most
of the Splunk installs out there. That, I realized, was why my old lib/ had two
PyMISP versions in it. One of them could never have run.

You can't engineer past this. You can only decide. Three real choices:

Drop PyMISP and talk to MISP's REST API directly with requests, which runs fine
on 3.9, and support basically everyone.

Keep the latest PyMISP but target only Splunk 10.2+ and Cloud 10.2+, where a
newer Python (3.13) is finally available, and use python.required to demand it.

Support both, with two code paths and more to maintain.

I took the second one. I wanted the current PyMISP and the current MISP feature
set, and I was OK saying "Splunk 10.2 and up." The mechanism is a single line,
python.required = 3.13, injected into the generated command and alert configs
so Splunk runs them on 3.13 instead of falling back to 3.9. UCC didn't expose
that setting, so I added a tiny post-build step to write it in. Five lines that
save you from a baffling ImportError in production.

The lesson I keep having to relearn: "use the latest version" is a decision
about your support matrix, not a checkbox. The moment a dependency's Python
floor climbs above your platform's Python, you're choosing who can't install
your app. Better to choose it on purpose than find out from a bug report.

## Fixing the actual design

With the platform settled, I finally cleaned up the sins from the prototype.

Templates instead of hardcoded types. The "everything is an IP" logic became a
set of templates: named profiles that say "this Splunk field becomes this MISP
type in this category, with these defaults." People edit them. They're not
locked in code.

But how do you keep a template correct when MISP servers differ and change over
time? The answer turned out to be nice. Let the server decide. MISP has a
describeTypes endpoint that returns, for that specific instance, every valid
type, every category, and which types are allowed in which category. So instead
of shipping a static list that goes stale, MISPFuse reads the connected
server's own taxonomy and checks against it. And the check is a warning, not a
wall. If an admin wants a combination I'd never pick, they can push it anyway.
Their server, their call.

Grouping you control. One-event-per-row became a choice: one event with many
attributes, one per row, or grouped by a field value. The "one big event" mode
needs to see all the results at once, so I built the command as an eventing
command (which gets the full set) and made the alert action, which naturally
receives every triggering event, the home for scheduled grouped pushes.

One core, two front doors. The command and the alert action are thin wrappers.
All the real work, reading the encrypted account, loading a template, grouping,
building attributes, keeping one bad row from killing the batch, lives in a
single shared library. Two ways to trigger it, one thing to maintain.

## Where it ended up

It's a real Splunk app now. Visible in the app bar, with a config UI, an
overview dashboard, a search command, and an alert action. You add your MISP
instances in the UI and the keys are encrypted, never in a file. You push
interactively with mispfusepush, or you attach the alert action to a saved
search for continuous export. Templates are yours to edit, and they're checked
live against your MISP server.

And it passes the checks that matter for publishing. No plaintext secrets, no
bundled virtualenv, no duplicate libraries, Python 3 only, cloud-vettable.

## A few things I'd tell myself at the start

Ship the embarrassing version, but know it's a prototype. The 30-line script
proved the idea. Believing it was the product would have been the mistake.

The platform's constraints are the design. Splunk's Python version, its
packaging rules, its credential handling. These aren't obstacles to route
around, they're the shape of the thing. UCC works because it leans into them.

Don't hand-roll what the framework generates. Encrypted credential storage and
REST handlers are exactly the code you'll get quietly wrong. Let the framework
own them and spend your time on the part that's actually yours. For me that was
the template model.

Check your dependency's Python floor against your platform's Python before you
commit. One mismatch quietly cuts off most of your users.

Let the source of truth be the source of truth. Reading MISP's describeTypes
instead of hardcoding a list means the app can't go stale against the servers
it talks to. Any time you want to embed a list somebody else maintains, don't.
Ask them at runtime.

MISPFuse went from a script I was slightly embarrassed by to an app I'm happy
to put my name on. The distance between those wasn't cleverness. It was
respecting the platform, making the constraints explicit, and letting the
framework carry the plumbing so I could focus on the one part that was mine.

If you've got a useful script that never left your laptop, the path to a real
tool is shorter than it looks. The tooling is good now. Go build the version
you'd put your name on.

If you're doing something similar with Splunk and UCC, I'm glad to compare
notes.
