# Security policy

## Supported versions

| Version | Security support |
|---|---|
| Latest `2.1.x` | Supported after the release artifact passes validation |
| `2.0.0-ucc` | Unsupported engineering milestone |
| `1.5.0-legacy` | Unsupported historical prototype |

Do not report defects in the historical versions as requests to patch those
branches. Report the defect against the current release unless the issue is
about inaccurate historical documentation.

## Reporting a vulnerability

Do not open a public issue containing API keys, session keys, internal URLs,
proxy credentials, Splunk tokens, MISP event data, or private search results.
Use the repository security-advisory feature or the maintainer's private
security contact.

A useful report includes:

- affected MISPFuse version;
- affected Splunk and MISP versions;
- deployment type;
- exact security impact;
- minimal reproduction steps;
- relevant logs with all secrets removed.

## Credential handling

The current application declares the MISP API key as an encrypted UCC field.
Splunk stores it through `storage/passwords`; the runtime reads the decrypted
value only when a command, alert action, or account test needs it.

This is reversible secret storage, not a password hash. Administrators with
sufficient Splunk or operating-system privilege may still access the secret.
Use a dedicated, least-privileged MISP automation key and rotate it after any
suspected Splunk-host compromise.

## Transport security

Production deployments should use HTTPS and certificate verification. The
current release retains HTTP and a disable-verification option for isolated
labs. These modes reduce transport assurance and may not be accepted for every
Splunk Cloud deployment.

## Legacy credential warning

The original traditional snapshot contains a real-looking API key and a private
MISP hostname. Revoke the key before any public commit. Deleting the file after
it has entered Git history is not sufficient.
