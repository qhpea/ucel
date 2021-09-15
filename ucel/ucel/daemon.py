from abc import ABC
import pkg_resources

named_objects = {}
for ep in pkg_resources.iter_entry_points(group='ucel.compute'):
   named_objects.update({ep.name: ep.load()})

class Daemon:
    """manages cluster"""
    
    def tick(self):
        "Update all of the computes and stuff in an orderly fassion"