#!/usr/bin/env python

"""
   Test of the scripts plugin

   Copyright 2010 Glencoe Software, Inc. All rights reserved.
   Use is subject to license terms supplied in LICENSE.txt

"""

import unittest, os, subprocess, StringIO
from path import path
from omero.cli import Context, BaseControl, CLI
from omero.plugins.script import ScriptControl
from omero.plugins.sessions import SessionsControl
from omero.plugins.upload import UploadControl
from omero.util.temp_files import create_path
from integration.library import ITest

omeroDir = path(os.getcwd()) / "build"


class TestScript(ITest):

    def cli(self):
        cli = CLI()
        cli.register("upload", UploadControl)
        cli.register("sessions", SessionsControl)
        cli.register("s", ScriptControl)
        return cli

    def test1(self):
        cli = self.cli()
        cli.invoke("s list -s localhost -u root".split(), strict=True)
        self.assertEquals(0, cli.rv)

    def testFullSession(self):
        cli = self.cli()
        p = create_path(suffix=".py")
        p.write_text("""
import omero, omero.scripts as s
from omero.rtypes import *

client = s.client("testFullSession", "simple ping script", s.Long("a").inout(), s.String("b").inout())
client.setOutput("a", rlong(0))
client.setOutput("b", rstring("c"))
client.closeSession()
""")
        args = ["s", "-q"] + self.login_args()
        #import pdb
        #pdb.set_trace()
        cli.invoke(args + ["upload", str(p)], strict=True) # Sets current script
        cli.invoke(args + ["list", "user"], strict=True)
        cli.invoke(args + ["serve", "user", "requests=1", "timeout=1", "background=true"], strict=True)
        cli.invoke(args + ["launch"], strict=True) # Uses current script

if __name__ == '__main__':
    unittest.main()