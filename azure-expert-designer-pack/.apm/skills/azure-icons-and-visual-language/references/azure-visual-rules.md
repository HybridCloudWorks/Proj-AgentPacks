# Azure Visual Rules

House style for this pack: Helvetica, icon styles copied unchanged from draw.io's Azure library (`azure2`), light neutral containers, blue numbered badges for complex diagrams, and explicit legends. Keep labels legible at the expected output size.

Icon geometry:

- copy the palette style that `check_drawio.py --find "<product>"` in `diagram-validation-and-evidence` prints, `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/<category>/<File_Name>.svg;`, and append only typography and label placement; the palette's `points=[...]` are optional connection points that do not change how the icon draws;
- "48 px" means 48 px on the icon's longest side, with `aspect=fixed` and the other side from the palette's aspect ratio; scope icons in frame corners are 24 px on the longest side;
- never add `whiteSpace=wrap` to an icon style; break a long label with `<br>` instead;
- use a consistent 120 px category or service tile only where the diagram uses tiles.

Containment: a draw.io cell has exactly one parent, so decide which hierarchy parents it.

- Network containment wins. A VNet (`container=1`) parents its subnets, and a subnet (`container=1`) parents the resources deployed into it. Each VNet sits inside exactly one region frame.
- A subscription or resource group frame is a real container (`container=1`) only for cells that truly belong to it.
- When ownership and network disagree, for example a private endpoint or gateway in a different resource group from its VNet, parent the resource to the network boundary it is deployed into, and show its resource group in its label or in a decorative `container=0` frame. This is the shared rule in `drawio-core-generation` workflow step 4.
- PaaS reached through a private endpoint stays outside the VNet, and App Service with regional VNet integration stays outside the VNet with an outbound edge into its delegated subnet.
- Region, zone, governance and "global resources" frames are decorative (`container=0`) unless children must move with them. A `container=0` frame never has child cells: place cells over it geometrically and parent them to the real container around it.
- Zones are labels on zone-redundant resources, not frames, and a subnet is never inside a zone frame.

Spacing and placement:

- keep at least 30 px inside boundaries and align coordinates to 10 px increments;
- put each scope icon in its frame's top-left corner with the frame's name as the icon's label, to the right of the icon;
- label external actors outside the Azure boundary, normally above or left of the main flow.

Microsoft's icon guidance (https://learn.microsoft.com/azure/architecture/icons/) says to include the product name close to the icon, use the icons as they appear in Azure, not crop, flip, rotate, distort or change their shape, and not use Microsoft product icons for your own product or service. Check the shared icon catalog, and Microsoft's current download when the catalog has no icon, before adding a new service.
