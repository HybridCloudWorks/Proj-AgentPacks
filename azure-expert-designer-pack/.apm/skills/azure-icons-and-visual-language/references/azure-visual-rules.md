# Azure Visual Rules

The supplied Azure Designer references use Helvetica, Azure2 image styles, light neutral containers, blue numbered badges for complex diagrams, and explicit legends. Keep labels legible at the expected output size.

Recommended boundary behavior:

- real subscription, resource group, VNet, and subnet groups use `container=1` and parent their children;
- decorative region or governance frames use `container=0` when children must not move with the frame;
- keep at least 30 px inside boundaries and align coordinates to 10 px increments;
- use 48 px service icons and a consistent 120 px category/service tile where the diagram uses tiles;
- label external actors outside the Azure boundary, normally above or left of the main flow.

Microsoft's official icon guidance says to use icons as they appear in Azure, place a product label nearby, and not crop, flip, rotate, distort, or use product icons for custom products. Verify the current official icon catalog before adding a new service.
