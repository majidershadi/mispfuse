import os,sys,re
from keys import misp_url, misp_key, misp_verifycert
from os.path import dirname
ta_name = 'mispfuse'
pattern = re.compile(r'[\\/]etc[\\/]apps[\\/][^\\/]+[\\/]bin[\\/]?$')
new_paths = [path for path in sys.path if not pattern.search(path) or ta_name in path]
new_paths.append(os.path.join(dirname(dirname(__file__)), "lib"))
new_paths.insert(0, os.path.sep.join([os.path.dirname(__file__), ta_name]))
sys.path = new_paths
from splunklib.searchcommands import (
    Configuration,
    Option,
    StreamingCommand,
    dispatch,
    validators,
)
from pymisp import (
    PyMISP,
    MISPEvent,
    MISPAttribute,
    MISPTag,
)
@Configuration()
class MISPFuser(StreamingCommand):
	def stream(self,records):
		misp= PyMISP(misp_url,
                misp_key,
                misp_verifycert)
		for record in records:
			events = MISPEvent()
			events.published = True
			if "publish" in record:
				events.published = bool(record["publish"])
			events.info= "Raise Up with MISPFuse From Splunk"
			if "info" in record:
				events.info= record["info"]
			events.threat_level_id = 2
			if "date" in record:
				events.date=record["date"]
			events.analysis = 1
			if "state" in record:
				events.analysis = int(record["state"])
			events.orgc_id=33
			events.org_id=33
			events.distribution=2
			if "distribution" in record:
				events.distribution=int(record["distribution"])
            #events.published=True
			category_at = 'Network activity'
			if "category" in record:
				category_at = record["category"]
			if category_at == 'Network activity':
				type_at = 'ip-src'
			else:
				type_at = record['attrib-type']
			value_at = record["target"]
			comment_at = "Malicious IP Address (v4)"
			if "comment" in record:
				comment_at = record["comment"]
			events.add_attribute(type=type_at ,
                    value=value_at ,
                    category=category_at ,
                    disable_correlation=True ,
                    comment = comment_at)
			tag_list= ['MYORGANIZATION']
			if "a_tag" in record:
				tag_list.append(record["a_tag"])
			for tag_at in tag_list:
				events.add_tag(tag_at)
			event_res=misp.add_event(events,pythonify=True)
			record["resualt"] = "event Added"
			yield record
#Main
dispatch(MISPFuser, sys.argv, sys.stdin, sys.stdout, __name__)

