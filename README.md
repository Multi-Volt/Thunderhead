# Thunderhead
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


This research endeavor, conducted by __Dr. John LaRocco__, __Dr. Qudsia Tahmina__, and __John Simonis__ at The Ohio State University, is dedicated to the development of a novel fire extinguishing device. Specifically, the primary objective of this project is to construct a system that can be juxtaposed with a conventional vortex ring launcher. Electrolytic solution is aersolized and mixed in with the vortex ring creation and dispersed through the air.
## Requirements
### Software
- [Git](https://git-scm.com/downloads)
- [Arduino IDE](https://www.arduino.cc/en/software)
- [FluidX3D](https://github.com/ProjectPhysX/FluidX3D)
- [Python](https://www.python.org/)
Some Python modules are required for this project to work on your computer. The easiest way to install the required Python packages is to use use the following command:
```bash
pip install numpy pandas openpyxl matplotlib seaborn pillow opencv-python trimesh
```
### Hardware
- [TH-BOM](https://github.com/Multi-Volt/Thunderhead/tree/main/FLOOD-BOM/)
- Screw Driver
# Table of contents
- [Models & Construction](#models)
- [Data](#data)
- [Datalogger](#datalogger)
- [Thunderhead Equations](#thunderhead-equations)
- [Thunderhead MCU](#thunderhead-mcu)
- [Thunderhead Media](#thunderhead-media)
- [License](#license)
## <a  id ="models"></a>Models & Construction
For this project, all pertinent 3D models are housed in the [TH-3DF](https://github.com/Multi-Volt/Thunderhead/tree/main/TH-3DF) directory. These 3D models are used for FluidX3D simulations.
### Details
There are two different prototypes that were tested during the duration of the Thunderhead project. One is a simple diaphragm based vortex ring launcher and the other is one using compressed air. A good way to identify all the codes is as follows:
- P1: Compressed Air with aerosolized electrolytic solution.
- P2: Diaphragm with aerosolized electrolytic solution.
- P3: Compressed Air without aersolized electrolytic solution.
- P4: Diaphragm without aerosolized electrolytic solution.

The construction of the vortex ring launcher is mostly the same for each prototype. It involves cutting out a circle at the end of a large bucket leaving a 1 1/2 inch gap between the outer edge of the bucket and the cut hole. The diapgraghm is constructed out of some thin polypropylene film duct taped to the edge of the bucket with two bungie cords used for spring tension. The Compressed air design uses standard quick fitting connectors with the lid of the bucket being epoxied on.
[(Back to top)](#table-of-contents)
### Wiring
You can find the schematics for this in [TH-Schematics](https://github.com/Multi-Volt/Thunderhead/tree/main/TH-Schematics). The wiring for this project is very simple.

[(Back to top)](#table-of-contents)
## Data
You can find the data for this in [TH-Data](https://github.com/Multi-Volt/Thunderhead/tree/main/TH-Data). The data for this project includes all individual matrices and also heatmap plots for each matrix.

[(Back to top)](#table-of-contents)
## Datalogger
This project currently uses a compiled Datalogger from a previous research project from this team. Currently, this binary is only compiled for Windows systems and is present within the [TH-Datalogger](https://github.com/Multi-Volt/Thunderhead/tree/main/TH-Datalogger) folder.

[(Back to top)](#table-of-contents)
## Thunderhead Equations
### Navier-Stokes Equations:
#### Incompressible Flow
1. **Continuity Equation:**

   $\nabla \cdot \mathbf{u} = 0$

   This equation ensures mass conservation, where $\mathbf{u}$ is the velocity vector field of the fluid.
2. **Momentum Equation:**

   $\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} \right) = -\nabla p + \mu \nabla^2 \mathbf{u} + \mathbf{f}$

   - $\rho$: Fluid density
   - $\mathbf{u}$: Velocity vector field
   - $t$: Time
   - $p$: Pressure
   - $\mu$: Dynamic viscosity
   - $\nabla^2 \mathbf{u}$: Laplacian of the velocity field (representing viscous diffusion)
   - $\mathbf{f}$: External forces (e.g., gravity)
#### Compressible Flow
1. **Continuity Equation:**

   $\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{u}) = 0$

   - This accounts for changes in density $\rho$ over time.
2. **Momentum Equation:**

   $\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} \right) = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \mathbf{f}$

   - $\boldsymbol{\tau}$: Stress tensor, which includes both viscous and pressure contributions.
3. **Energy Equation:**

   $\frac{\partial E}{\partial t} + \nabla \cdot \left( (E + p)\mathbf{u} \right) = \nabla \cdot (\mathbf{u} \cdot \boldsymbol{\tau}) + \nabla \cdot (\kappa \nabla T) + \mathbf{u} \cdot \mathbf{f}$

   - $E$: Total energy per unit volume
   - $T$: Temperature
   - $\kappa$: Thermal conductivity


## Thunderhead MCU
There is some deprecated microcontroller code for this project present in [TH-MCU](https://github.com/Multi-Volt/Thunderhead/tree/main/TH-MCU)

[(Back to top)](#table-of-contents)
## Thunderhead Media
For this project, all pertinent images and other media are housed in the [TH-Media](https://github.com/Multi-Volt/Thunderhead/tree/main/TH-Media) directory.
# License
The MIT License (MIT) 2024 - [Dr. John LaRocco](https://github.com/javeharron/), [Dr. Qudsia Tahmina](https://github.com/tahminaq), [John Simonis](https://github.com/Multi-Volt/). Please have a look at the [LICENSE.md](LICENSE) for more details.

[(Back to top)](#table-of-contents)
