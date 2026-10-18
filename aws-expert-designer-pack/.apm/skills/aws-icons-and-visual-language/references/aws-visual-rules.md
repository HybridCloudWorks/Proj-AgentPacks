# AWS Visual Rules

Use the AWS4 namespace and current icon library. The supplied AWS rules establish these defaults:

- `fontFamily=Helvetica` for all text; sketch attributes only when the user explicitly requests sketch mode;
- title 30 px bold, subtitle 16 px, group 14 px bold, container 12 px bold, service 10 px, edge 11 px;
- Region groups use `container=0` and are decorative; VPCs, Availability Zones, and subnets use real containment only when children should move with them;
- VPC boundary color is `#8C4FFF`, public subnet `#248814`, private subnet `#147EBA`, and Region `#00A4A6`; group text color matches the stroke;
- structural colors use `light-dark()` and `fillStyle=auto` when dark-mode compatibility is required; do not hardcode `mxGraphModel background`;
- use neutral visible containers for external actors below the title block; use dashed auxiliary groups for cross-cutting services that are not primary flow steps.

AWS's official icon page states that AWS-approved icon packages are updated quarterly and warns that third-party libraries may contain legacy icon sets. Recheck the current package before adding a service absent from the installed library.
