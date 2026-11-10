# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Independent BREP validation of initial viewer travel endpoints after building."""
import json
from pathlib import Path
from koala_hardware.audit import check_scene


def main():
    root=Path(__file__).resolve().parents[2]
    source=root/'build/viewer/mechanical-limits.json';data=json.loads(source.read_text());results=[]
    for pose,record in data['poses'].items():
     for axis,lim in record['limits']['bounds'].items():
      for end in ('min','max'):
       q={'roll':0,'pitch':0,'knee':0};q[axis]=lim[end]
       count=check_scene(pose,(q['roll'],q['pitch'],q['knee']))
       results.append({'pose':pose,'axis':axis,'endpoint':end,'degrees':lim[end],'boolean_pairs':count})
       print('PASS',results[-1],flush=True)
    (root.parent/'docs/design/manufacturing/travel-endpoints.json').write_text(json.dumps({'scope':'BREP checks of the twelve initial grouped slider endpoints; dynamic combinations are searched by the viewer mesh engine. No loaded or continuous-sweep proof.','endpoints':results},indent=2)+'\n')


if __name__ == "__main__":main()
