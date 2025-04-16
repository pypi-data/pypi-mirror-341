# pypeto
PyQt-based tabular user interface for designing and implementing control screens for EPICS (CA and PVA) and LiteServer devices.

Supported:
 - control of EPICS PVs and liteServer PVs,
 - automatic page generation,
 - merged cells, adjustable size of rows and columns, fonts and colors,
 - horizontal and vertical slider widgets,
 - configuration using python,
 - macro substitution from command line: single configuration file can be used for many similar devices,
 - embedding displays of other programs to a range of cells,
 - plotting of selected cells using pvplot,
 - content-driven cell coloring,
 - snapshots: full page can be saved and the selected cells could be restored from the saved snapshots,
 - slicing of vector parameters.

![simScope](./docs/pypeto_simScopePVA.png)

## Tests:
Control of a simulated oscilloscope from EPICS Channel Access infrastructure 
[link](https://epics.anl.gov/modules/soft/asyn/R4-38/asynDriver.html#testAsynPortDriverApp):<br>
`python -m pypeto -cconfig -fsimScope -e`

Control of a simulated oscilloscope from EPICS PVAccess infrastructure [link](https://github.com/ASukhanov/p4pex):<br>
`python -m pypeto -cconfig -fsimScopePVA -e`

Control of a peak simulator from LiteServer infrastructure :<br>
`python -m pypeto -cconfig -fpeakSimulator -e`

### Control of the litePeakSimulator
The testing requires sattellite module [litePeakSimulator](https://github.com/ASukhanov/liteServer).<br>
Start the litePeakSimulator liteserver on localhost if it is not running yet.<br>
`python3 -m liteserver.device.litePeakSimulator -ilo -p9710`

Connect to litePeakSimulator from pypeto:<br>
`python3 -m pypeto -aLITE 'localhost;9710:dev1'&`

Using pypeto configuration file peakSimulator_pp.py:<br>
`cd github/pypeto`<br>
`python3 -m pypeto -f peakSimulator`


