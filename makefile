
all: colcon-build

colcon-build:
	colcon build --symlink-install

clean:
	rm -rf build/ log/ install/
	
devbox-install:
	# Need sudo here for when password authentication is on
	cd setup && sudo ansible-playbook \
		--connection=local \
		--inventory 127.0.0.1, \
		--limit 127.0.0.1 devbox.yaml