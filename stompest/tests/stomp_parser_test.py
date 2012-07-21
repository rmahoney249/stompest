# -*- coding: iso-8859-1 -*-
"""
Copyright 2012 Mozes, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import unittest                                 

from stompest.protocol.frame import StompFrame
from stompest.protocol.parser import StompParser
from stompest.error import StompFrameError
from stompest.protocol import commands

class StompParserTest(unittest.TestCase):
    def test_frameParse_succeeds(self):
        message = {
            'cmd': 'SEND',
            'headers': {'foo': 'bar', 'hello ': 'there-world with space ', 'empty-value':'', '':'empty-header', 'destination': '/queue/blah'},
            'body': 'some stuff\nand more'
        }
        frame = StompFrame(**message)
        parser = StompParser()
        
        parser.add(frame.pack())
        self.assertEqual(parser.getMessage().__dict__, {'cmd': frame.cmd, 'headers': frame.headers, 'body': frame.body})
        self.assertEqual(parser.getMessage(), None)
        
    def test_frame_without_header_or_body_succeeds(self):
        parser = StompParser()
        parser.add(commands.disconnect().pack())
        msg = parser.getMessage()
        self.assertEqual(msg.__dict__, {'cmd': 'DISCONNECT', 'headers': {}, 'body': ''})

    def test_frames_with_optional_newlines_succeeds(self):
        parser = StompParser()
        frame = '\n%s\n' % commands.disconnect().pack()
        parser.add(2 * frame)
        for _ in xrange(2):
            self.assertEqual(parser.getMessage().__dict__, {'cmd': 'DISCONNECT', 'headers': {}, 'body': ''})
        self.assertEqual(parser.getMessage(), None)

    def test_getMessage_returns_None_if_not_done(self):
        parser = StompParser()
        self.assertEqual(None, parser.getMessage())
        parser.add('CONNECT')
        self.assertEqual(None, parser.getMessage())
        
    def test_processLine_throws_FrameError_on_invalid_command(self):
        parser = StompParser()
        
        self.assertRaises(StompFrameError, lambda: parser.add('HELLO\n'))

    def test_processLine_throws_FrameError_on_header_line_missing_separator(self):
        parser = StompParser()
        parser.add('SEND\n')
        self.assertRaises(StompFrameError, lambda: parser.add('no separator\n'))

if __name__ == '__main__':
    unittest.main()
