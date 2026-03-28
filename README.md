# README
## All graphs generated in [main.py](https://github.com/zacMadison/Regression-Analysis-ZachMadison-Public/blob/main/main.py)
- Can be run to generate new graphs with different axis variables
- Results in [Graphs](https://github.com/zacMadison/Regression-Analysis-ZachMadison-Public/tree/main/Graphs)

## DOCKER INSTRUCTIONS
### Building Image
- from the root directory run:  "docker build -t [name] ."
### Running Image
- run "docker run -v [Directory to save at]:/Regression-Analysis-ZachMadison-Public/output --rm -it [image name]"
	- --rm: optional arg to remove container once run has been completed
	- output from program should be added to chosen directory as "output.png"
