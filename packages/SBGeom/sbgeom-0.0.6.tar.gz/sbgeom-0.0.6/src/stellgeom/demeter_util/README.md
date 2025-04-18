#### Demeter Utilities


These are just a couple of utilities that are needed for building the DEMETER neutron code. They have been separated
because the geometry tool StellGeom uses them as well and needs to be separate from DEMETER.

This project doesn't do anything by itself; it's separated so it can be used and added wherever required.

### Using git subtree

To add a git subtree of this repository to your project use:

```
 git remote add subtree_demeter_util git@gitlab.tue.nl:s1668021/demeter-utilities.git
 git subtree add --prefix=demeter_util/ subtree_demeter_util main
```

This will create a copy of the repository at the demeter_util folder.

To update to the newest version, use 

```
 git subtree pull --prefix=demeter_util subtree_demeter_util main
```

To push changes to these files back to this repository, use 

```
git subtree push --prefix=demeter_util subtree_demeter_util main
```
(pushes it to the main branch)
