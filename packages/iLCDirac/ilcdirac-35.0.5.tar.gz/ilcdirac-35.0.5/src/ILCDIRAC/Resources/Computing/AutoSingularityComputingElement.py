#
# Copyright (c) 2009-2022 CERN. All rights nots expressly granted are
# reserved.
#
# This file is part of iLCDirac
# (see ilcdirac.cern.ch, contact: ilcdirac-support@cern.ch).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# In applying this licence, CERN does not waive the privileges and
# immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""This module implements an extension of the SingularityComputingElement that automatically deduces the OS image to use for a given job."""

from pprint import pformat

from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Resources.Computing.SingularityComputingElement import SingularityComputingElement

from ILCDIRAC.Core.Utilities.DetectOS import NativeMachine

class AutoSingularityComputingElement(SingularityComputingElement):
    """A computing element based on singularity that will automatically deduce the OS container it should run based on job
parameters."""

    def __init__(self, ceUniqueID):
        """Standard constructor."""
        super().__init__(ceUniqueID)

    def submitJob(self, executableFile, proxy=None, **kwargs):
       """Figure out the rootImage and call super submitJob"""
       self.log.always("The kwargs are", pformat(kwargs))

       jobParameters = kwargs.get("jobParams")

       # If the ApptainerImage is defined in the JobParameters / JDL we use it
       if theImage := jobParameters.get("ApptainerImage"):
           self.log.info(f"And we are using {theImage!r} from jobParameters")
           self._SingularityComputingElement__root = theImage
           return super().submitJob(executableFile, proxy=proxy, **kwargs)

       # we get the list of SoftwarePackages from the jobParameters
       apps = []
       if softPackages := jobParameters.get('SoftwarePackages'):
           if isinstance(softPackages, str):
               apps = [softPackages]
           elif isinstance(softPackages, list):
               apps = softPackages

       # Figure out the platform we are using since we have platform in the jobparameters
       # this is needed for finding the software package options
       jobConfig = ""
       if jobConfig := jobParameters.get("SystemConfig"):
           pass
       elif jobConfig := jobParameters.get("Platform"):
           pass
       else:
           jobConfig = NativeMachine().CMTSupportedConfig()[0]

       ops = Operations()
       # the default os we use, should be taken from VO specific operations section like this
       theOS = ops.getValue("/Software/DefaultSingularityOS", "el9")
       self.log.info("We found the defaultOS to use", theOS)
       if apps:
           # if we have applications, chec, if there is a specific image to use, or other OS to use
           appName, appVersion= apps[0].split('.')
           # check if the software app has an ApptainerImage defined and use that
           if theImage := ops.getValue(f'/AvailableTarBalls/{jobConfig}/{appName}/{appVersion}/ApptainerImage', None):
               self.log.info(f"And we are using {theImage!r} from the {appName}/{appVersion}")
               self._SingularityComputingElement__root = theImage
               return super().submitJob(executableFile, proxy=proxy, **kwargs)

           theOS = ops.getValue(f'/AvailableTarBalls/{jobConfig}/{appName}/{appVersion}/OS', theOS)
           self.log.info(f"Based on /AvailableTarBalls/{jobConfig}/{appName}/{appVersion}/OS")
           self.log.info(f"We are now going to use {theOS}")

       theDefaultImage = ops.getValue("/Software/Containers/default")
       self.log.info(f"The default image would be {theDefaultImage}")

       theImage = ops.getValue(f"/Software/Containers/{theOS}", theDefaultImage)
       self.log.info(f"And we are using: {theImage}")

       self._SingularityComputingElement__root = theImage
       return super().submitJob(executableFile, proxy=proxy, **kwargs)
