all: colcon-build

colcon-build:
	colcon build --symlink-install

clean:
	rm -rf build/ log/ install/