# OpenCraft -- tools to aid developing and hosting free software projects
# Copyright (C) 2015 OpenCraft <xavier@opencraft.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# Variables ###################################################################

GET = wget -qO
CDNFONTS = https://fortawesome.github.io/Font-Awesome/assets/


# Files #######################################################################

all: js_external font-awesome-4.4.0.zip
 
font-awesome-4.4.0.zip:
	$(GET) $@ $(CDNFONTS)/font-awesome-4.4.0.zip
	unzip font-awesome-4.4.0.zip -x *scss* *less* *.txt
	cp font-awesome-4.4.0/fonts/* fonts/
	cp font-awesome-4.4.0/css/* css/
	rm -r font-awesome-4.4.0*
js_external:
	$(MAKE) -C js
