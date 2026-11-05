# Batch 9 - relay-free inquiry capture.
# Replaces the dead FormSubmit relay with a compose-and-handoff form: the visitor
# gets a prefilled WhatsApp message and email, plus a copy button. No third-party
# service is involved, so no relay outage can drop an inquiry.
import base64
import pathlib
import re
import sys

NEW_JS = base64.b64decode(
    "LyogSW5xdWlyeSBmb3JtIHYzIC0gcmVsYXktZnJlZS4KICAgTm90aGluZyBpcyBwb3N0ZWQgdG8gYSB0aGlyZC1wYXJ0eSBzZXJ2aWNlLCBzbyBubyByZWxheSBvdXRhZ2UgY2FuIHN3YWxsb3cgYW4KICAgaW5xdWlyeS4gT24gc3VibWl0IHRoZSB2aXNpdG9yJ3Mgb3duIGRldGFpbHMgYXJlIGNvbXBvc2VkIGludG8gYSByZWFkeS10by1zZW5kCiAgIFdoYXRzQXBwIG1lc3NhZ2UgYW5kIGEgcmVhZHktdG8tc2VuZCBlbWFpbCwgYW5kIGEgcGFuZWwgb2ZmZXJzIGJvdGggcGx1cyBhCiAgIGNvcHkgYnV0dG9uLiBXb3JrcyB3aXRoIG9yIHdpdGhvdXQgYSBjb25maWd1cmVkIGRlc2t0b3AgbWFpbCBjbGllbnQuICovCihmdW5jdGlvbiAoKSB7CiAgaWYgKHdpbmRvdy5fX2psY2NJbnF1aXJ5Rm9ybUxvYWRlZCkgeyByZXR1cm47IH0KICB3aW5kb3cuX19qbGNjSW5xdWlyeUZvcm1Mb2FkZWQgPSB0cnVlOwoKICB2YXIgRU1BSUwgPSAneHh5MTM5OTI4NTkxNjZAZ21haWwuY29tJzsKICB2YXIgV0EgPSAnaHR0cHM6Ly93YS5tZS84NjE1MzM5MDA1MTkzJzsKCiAgZnVuY3Rpb24gdmFsKGYsIG4pIHsKICAgIHZhciBlbCA9IGYucXVlcnlTZWxlY3RvcignW25hbWU9IicgKyBuICsgJyJdJyk7CiAgICByZXR1cm4gZWwgPyBTdHJpbmcoZWwudmFsdWUgfHwgJycpLnRyaW0oKSA6ICcnOwogIH0KCiAgZnVuY3Rpb24gY29tcG9zZShmKSB7CiAgICB2YXIgbmFtZSA9IHZhbChmLCAnbmFtZScpLCBjb21wYW55ID0gdmFsKGYsICdjb21wYW55Jyk7CiAgICB2YXIgZW1haWwgPSB2YWwoZiwgJ2VtYWlsJyksIHBob25lID0gdmFsKGYsICdwaG9uZScpLCBtc2cgPSB2YWwoZiwgJ21lc3NhZ2UnKTsKICAgIHZhciBzdWJqZWN0ID0gJ1NvbGFyIGNhYmxlIGlucXVpcnkgLSAnICsgKGNvbXBhbnkgfHwgbmFtZSB8fCAnd2Vic2l0ZScpOwogICAgdmFyIGJvZHkgPSAnTmFtZTogJyArIG5hbWUgKyAnXG5Db21wYW55OiAnICsgY29tcGFueSArICdcbkVtYWlsOiAnICsgZW1haWwgKwogICAgICAnXG5QaG9uZSAvIFdoYXRzQXBwOiAnICsgcGhvbmUgKyAnXG5cblJlcXVpcmVtZW50OlxuJyArIG1zZyArCiAgICAgICdcblxuUGFnZTogJyArIGxvY2F0aW9uLmhyZWY7CiAgICByZXR1cm4gewogICAgICBzdWJqZWN0OiBzdWJqZWN0LAogICAgICBib2R5OiBib2R5LAogICAgICB3YTogV0EgKyAnP3RleHQ9JyArIGVuY29kZVVSSUNvbXBvbmVudChzdWJqZWN0ICsgJ1xuXG4nICsgYm9keSksCiAgICAgIG1haWw6ICdtYWlsdG86JyArIEVNQUlMICsgJz9zdWJqZWN0PScgKyBlbmNvZGVVUklDb21wb25lbnQoc3ViamVjdCkgKwogICAgICAgICcmYm9keT0nICsgZW5jb2RlVVJJQ29tcG9uZW50KGJvZHkpLAogICAgICBmdWxsOiAnVG86ICcgKyBFTUFJTCArICdcblN1YmplY3Q6ICcgKyBzdWJqZWN0ICsgJ1xuXG4nICsgYm9keQogICAgfTsKICB9CgogIGZ1bmN0aW9uIGNvcHlUZXh0KHRleHQsIGRvbmUpIHsKICAgIHZhciBmYWxsYmFjayA9IGZ1bmN0aW9uICgpIHsKICAgICAgdHJ5IHsKICAgICAgICB2YXIgdGEgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCd0ZXh0YXJlYScpOwogICAgICAgIHRhLnZhbHVlID0gdGV4dDsKICAgICAgICB0YS5zZXRBdHRyaWJ1dGUoJ3N0eWxlJywgJ3Bvc2l0aW9uOmZpeGVkO2xlZnQ6LTk5OTlweDt0b3A6MCcpOwogICAgICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQodGEpOwogICAgICAgIHRhLnNlbGVjdCgpOwogICAgICAgIGRvY3VtZW50LmV4ZWNDb21tYW5kKCdjb3B5Jyk7CiAgICAgICAgZG9jdW1lbnQuYm9keS5yZW1vdmVDaGlsZCh0YSk7CiAgICAgICAgZG9uZSgpOwogICAgICB9IGNhdGNoIChlKSB7IC8qIGxlYXZlIHRoZSBtZXNzYWdlIHZpc2libGUgZm9yIG1hbnVhbCBjb3B5ICovIH0KICAgIH07CiAgICBpZiAobmF2aWdhdG9yLmNsaXBib2FyZCAmJiBuYXZpZ2F0b3IuY2xpcGJvYXJkLndyaXRlVGV4dCkgewogICAgICBuYXZpZ2F0b3IuY2xpcGJvYXJkLndyaXRlVGV4dCh0ZXh0KS50aGVuKGRvbmUsIGZhbGxiYWNrKTsKICAgIH0gZWxzZSB7CiAgICAgIGZhbGxiYWNrKCk7CiAgICB9CiAgfQoKICBmdW5jdGlvbiBwYW5lbChmLCB0KSB7CiAgICB2YXIgb2xkID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2psY2Mtc2VuZC1wYW5lbCcpOwogICAgaWYgKG9sZCAmJiBvbGQucGFyZW50Tm9kZSkgeyBvbGQucGFyZW50Tm9kZS5yZW1vdmVDaGlsZChvbGQpOyB9CgogICAgdmFyIGJveCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpOwogICAgYm94LmlkID0gJ2psY2Mtc2VuZC1wYW5lbCc7CiAgICBib3guc2V0QXR0cmlidXRlKCdzdHlsZScsICdtYXJnaW4tdG9wOjE0cHg7cGFkZGluZzoxNnB4IDE4cHg7Ym9yZGVyLXJhZGl1czo4cHg7YmFja2dyb3VuZDojZWZmNmZmO2JvcmRlcjoxcHggc29saWQgIzkzYzVmZDtjb2xvcjojMWUzYTVmO2ZvbnQtc2l6ZToxNHB4O2xpbmUtaGVpZ2h0OjEuNicpOwogICAgYm94LmlubmVySFRNTCA9CiAgICAgICc8c3Ryb25nPllvdXIgaW5xdWlyeSBpcyByZWFkeSB0byBzZW5kLjwvc3Ryb25nPiBDaG9vc2Ugb25lIC0gd2UgcmVwbHkgdG8gd2hpY2hldmVyIHlvdSBwaWNrLicgKwogICAgICAnPGRpdiBzdHlsZT0ibWFyZ2luLXRvcDoxMnB4O2Rpc3BsYXk6ZmxleDtnYXA6MTBweDtmbGV4LXdyYXA6d3JhcCI+JyArCiAgICAgICc8YSBocmVmPSInICsgdC53YSArICciIGRhdGEtd2EtaW50YWtlPSIxIiB0YXJnZXQ9Il9ibGFuayIgcmVsPSJub29wZW5lciIgc3R5bGU9InBhZGRpbmc6MTFweCAxOHB4O2JvcmRlci1yYWRpdXM6NnB4O2JhY2tncm91bmQ6IzE2YTM0YTtjb2xvcjojZmZmO3RleHQtZGVjb3JhdGlvbjpub25lO2ZvbnQtd2VpZ2h0OjYwMCI+U2VuZCBvbiBXaGF0c0FwcCAoZmFzdGVzdCk8L2E+JyArCiAgICAgICc8YSBocmVmPSInICsgdC5tYWlsICsgJyIgc3R5bGU9InBhZGRpbmc6MTFweCAxOHB4O2JvcmRlci1yYWRpdXM6NnB4O2JhY2tncm91bmQ6IzI1NjNlYjtjb2xvcjojZmZmO3RleHQtZGVjb3JhdGlvbjpub25lO2ZvbnQtd2VpZ2h0OjYwMCI+U2VuZCBieSBlbWFpbDwvYT4nICsKICAgICAgJzxidXR0b24gdHlwZT0iYnV0dG9uIiBpZD0iamxjYy1jb3B5IiBzdHlsZT0icGFkZGluZzoxMXB4IDE4cHg7Ym9yZGVyLXJhZGl1czo2cHg7Ym9yZGVyOjFweCBzb2xpZCAjOTNjNWZkO2JhY2tncm91bmQ6I2ZmZjtjb2xvcjojMWUzYTVmO2ZvbnQtd2VpZ2h0OjYwMDtjdXJzb3I6cG9pbnRlciI+Q29weSB0aGUgdGV4dDwvYnV0dG9uPicgKwogICAgICAnPC9kaXY+JyArCiAgICAgICc8cCBzdHlsZT0ibWFyZ2luOjEycHggMCAwO2ZvbnQtc2l6ZToxMnB4O2NvbG9yOiM0NzU1NjkiPllvdXIgdGV4dCBpcyBhbHJlYWR5IGluc2lkZSBib3RoIGJ1dHRvbnMuIElmIG5laXRoZXIgb3BlbnMsIHVzZSBDb3B5IGFuZCBzZW5kIGl0IHRvICcgKwogICAgICBFTUFJTCArICcgb3IgV2hhdHNBcHAgKzg2IDE1MyAzOTAwIDUxOTMuPC9wPic7CgogICAgdmFyIGJ0biA9IGYucXVlcnlTZWxlY3RvcignYnV0dG9uW3R5cGU9InN1Ym1pdCJdJykgfHwgZi5xdWVyeVNlbGVjdG9yKCdidXR0b24nKTsKICAgIGlmIChidG4gJiYgYnRuLnBhcmVudE5vZGUpIHsgYnRuLnBhcmVudE5vZGUuaW5zZXJ0QmVmb3JlKGJveCwgYnRuLm5leHRTaWJsaW5nKTsgfQogICAgZWxzZSB7IGYuYXBwZW5kQ2hpbGQoYm94KTsgfQoKICAgIHZhciBjcCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdqbGNjLWNvcHknKTsKICAgIGlmIChjcCkgewogICAgICBjcC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGZ1bmN0aW9uICgpIHsKICAgICAgICBjb3B5VGV4dCh0LmZ1bGwsIGZ1bmN0aW9uICgpIHsKICAgICAgICAgIGNwLnRleHRDb250ZW50ID0gJ0NvcGllZCAtIG5vdyBwYXN0ZSBpdCc7CiAgICAgICAgfSk7CiAgICAgIH0pOwogICAgfQogICAgdHJ5IHsgYm94LnNjcm9sbEludG9WaWV3KHsgYmVoYXZpb3I6ICdzbW9vdGgnLCBibG9jazogJ2NlbnRlcicgfSk7IH0gY2F0Y2ggKGUpIHt9CiAgfQoKICBmdW5jdGlvbiBvblN1Ym1pdChlKSB7CiAgICB2YXIgZiA9IGUudGFyZ2V0OwogICAgaWYgKCFmIHx8ICFmLnF1ZXJ5U2VsZWN0b3IoJ1tuYW1lPSJtZXNzYWdlIl0nKSkgeyByZXR1cm47IH0KICAgIGUucHJldmVudERlZmF1bHQoKTsKICAgIHZhciB0ID0gY29tcG9zZShmKTsKICAgIHBhbmVsKGYsIHQpOwogIH0KCiAgZnVuY3Rpb24gd2lyZShmKSB7CiAgICBpZiAoIWYgfHwgZi5nZXRBdHRyaWJ1dGUoJ2RhdGEtamxjYy13aXJlZCcpID09PSAnMScpIHsgcmV0dXJuOyB9CiAgICBmLnNldEF0dHJpYnV0ZSgnZGF0YS1qbGNjLXdpcmVkJywgJzEnKTsKICAgIGYuc2V0QXR0cmlidXRlKCdkYXRhLWpsY2MtZm9ybScsICcxJyk7CiAgICBmLmFkZEV2ZW50TGlzdGVuZXIoJ3N1Ym1pdCcsIG9uU3VibWl0KTsKICB9CgogIGZ1bmN0aW9uIGV4aXN0aW5nRm9ybSgpIHsKICAgIHZhciBmID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignZm9ybVtkYXRhLWpsY2MtZm9ybV0nKSB8fAogICAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCdmb3JtW2FjdGlvbl49Im1haWx0bzoiXScpOwogICAgaWYgKGYpIHsgcmV0dXJuIGY7IH0KICAgIHZhciBhbGwgPSBkb2N1bWVudC5nZXRFbGVtZW50c0J5VGFnTmFtZSgnZm9ybScpOwogICAgZm9yICh2YXIgaSA9IDA7IGkgPCBhbGwubGVuZ3RoOyBpKyspIHsKICAgICAgaWYgKGFsbFtpXS5xdWVyeVNlbGVjdG9yKCdbbmFtZT0ibWVzc2FnZSJdJykpIHsgcmV0dXJuIGFsbFtpXTsgfQogICAgfQogICAgcmV0dXJuIG51bGw7CiAgfQoKICBmdW5jdGlvbiBtb3VudCgpIHsKICAgIHZhciBmb3VuZCA9IGV4aXN0aW5nRm9ybSgpOwogICAgaWYgKGZvdW5kKSB7IHdpcmUoZm91bmQpOyByZXR1cm47IH0KICAgIGlmIChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnamxjYy1pbnF1aXJ5JykpIHsgcmV0dXJuOyB9CgogICAgdmFyIHNlY3Rpb24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdzZWN0aW9uJyk7CiAgICBzZWN0aW9uLmlkID0gJ2psY2MtaW5xdWlyeSc7CiAgICBzZWN0aW9uLnNldEF0dHJpYnV0ZSgnc3R5bGUnLCAncGFkZGluZzo0MHB4IDE2cHg7YmFja2dyb3VuZDojZjFmNWY5O2ZvbnQtZmFtaWx5OnN5c3RlbS11aSwtYXBwbGUtc3lzdGVtLFNlZ29lIFVJLFJvYm90byxBcmlhbCxzYW5zLXNlcmlmJyk7CiAgICBzZWN0aW9uLmlubmVySFRNTCA9IFsKICAgICAgJzxkaXYgc3R5bGU9Im1heC13aWR0aDo5NjBweDttYXJnaW46MCBhdXRvIj4nLAogICAgICAnPGgyPlJlcXVlc3QgYSBRdW90ZTwvaDI+JywKICAgICAgJzxwIHN0eWxlPSJtYXJnaW46MCAwIDE4cHg7Y29sb3I6IzQ3NTU2OTtmb250LXNpemU6MTRweCI+U2VuZCB5b3VyIHNwZWNpZmljYXRpb24gYW5kIHF1YW50aXR5IC0gd2UgcmVwbHkgd2l0aCBwcmljZSwgbGVhZCB0aW1lIGFuZCBwYWNraW5nLjwvcD4nLAogICAgICAnPGZvcm0gZGF0YS1qbGNjLWZvcm0gYWN0aW9uPSJtYWlsdG86JyArIEVNQUlMICsgJz9zdWJqZWN0PVNvbGFyJTIwY2FibGUlMjBpbnF1aXJ5IiBtZXRob2Q9InBvc3QiIGVuY3R5cGU9InRleHQvcGxhaW4iPicsCiAgICAgICc8ZGl2IHN0eWxlPSJkaXNwbGF5OmZsZXg7Z2FwOjEycHg7ZmxleC13cmFwOndyYXA7bWFyZ2luLWJvdHRvbToxMnB4Ij4nLAogICAgICAnPGxhYmVsIHN0eWxlPSJmbGV4OjEgMSAyMjBweDtmb250LXNpemU6MTJweDtjb2xvcjojMzM0MTU1Ij5Zb3VyIE5hbWUgKjxicj48aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0ibmFtZSIgcmVxdWlyZWQgc3R5bGU9IndpZHRoOjEwMCU7cGFkZGluZzoxMHB4O21hcmdpbi10b3A6NXB4O2JvcmRlcjoxcHggc29saWQgI2NiZDVlMTtib3JkZXItcmFkaXVzOjZweCI+PC9sYWJlbD4nLAogICAgICAnPGxhYmVsIHN0eWxlPSJmbGV4OjEgMSAyMjBweDtmb250LXNpemU6MTJweDtjb2xvcjojMzM0MTU1Ij5Db21wYW55PGJyPjxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJjb21wYW55IiBzdHlsZT0id2lkdGg6MTAwJTtwYWRkaW5nOjEwcHg7bWFyZ2luLXRvcDo1cHg7Ym9yZGVyOjFweCBzb2xpZCAjY2JkNWUxO2JvcmRlci1yYWRpdXM6NnB4Ij48L2xhYmVsPicsCiAgICAgICc8L2Rpdj4nLAogICAgICAnPGRpdiBzdHlsZT0iZGlzcGxheTpmbGV4O2dhcDoxMnB4O2ZsZXgtd3JhcDp3cmFwO21hcmdpbi1ib3R0b206MTJweCI+JywKICAgICAgJzxsYWJlbCBzdHlsZT0iZmxleDoxIDEgMjIwcHg7Zm9udC1zaXplOjEycHg7Y29sb3I6IzMzNDE1NSI+RW1haWwgKjxicj48aW5wdXQgdHlwZT0iZW1haWwiIG5hbWU9ImVtYWlsIiByZXF1aXJlZCBzdHlsZT0id2lkdGg6MTAwJTtwYWRkaW5nOjEwcHg7bWFyZ2luLXRvcDo1cHg7Ym9yZGVyOjFweCBzb2xpZCAjY2JkNWUxO2JvcmRlci1yYWRpdXM6NnB4Ij48L2xhYmVsPicsCiAgICAgICc8bGFiZWwgc3R5bGU9ImZsZXg6MSAxIDIyMHB4O2ZvbnQtc2l6ZToxMnB4O2NvbG9yOiMzMzQxNTUiPldoYXRzQXBwIC8gUGhvbmU8YnI+PGlucHV0IHR5cGU9InRleHQiIG5hbWU9InBob25lIiBzdHlsZT0id2lkdGg6MTAwJTtwYWRkaW5nOjEwcHg7bWFyZ2luLXRvcDo1cHg7Ym9yZGVyOjFweCBzb2xpZCAjY2JkNWUxO2JvcmRlci1yYWRpdXM6NnB4Ij48L2xhYmVsPicsCiAgICAgICc8L2Rpdj4nLAogICAgICAnPGxhYmVsIHN0eWxlPSJkaXNwbGF5OmJsb2NrO2ZvbnQtc2l6ZToxMnB4O2NvbG9yOiMzMzQxNTUiPlJlcXVpcmVtZW50ICo8YnI+PHRleHRhcmVhIG5hbWU9Im1lc3NhZ2UiIHJlcXVpcmVkIHN0eWxlPSJ3aWR0aDoxMDAlO21pbi1oZWlnaHQ6MTEwcHg7cGFkZGluZzoxMHB4O21hcmdpbi10b3A6NXB4O2JvcmRlcjoxcHggc29saWQgI2NiZDVlMTtib3JkZXItcmFkaXVzOjZweCIgcGxhY2Vob2xkZXI9IkNhYmxlIHR5cGUgYW5kIHNpemUsIHF1YW50aXR5IGluIG1ldHJlcywgZGVzdGluYXRpb24gcG9ydCI+PC90ZXh0YXJlYT48L2xhYmVsPicsCiAgICAgICc8ZGl2IHN0eWxlPSJtYXJnaW4tdG9wOjEycHg7ZGlzcGxheTpmbGV4O2dhcDoxMHB4O2ZsZXgtd3JhcDp3cmFwIj4nLAogICAgICAnPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIHN0eWxlPSJwYWRkaW5nOjEycHggMjJweDtib3JkZXI6MDtib3JkZXItcmFkaXVzOjZweDtiYWNrZ3JvdW5kOiMyNTYzZWI7Y29sb3I6I2ZmZjtmb250LXNpemU6MTVweDtmb250LXdlaWdodDo2MDA7Y3Vyc29yOnBvaW50ZXIiPlNlbmQgSW5xdWlyeTwvYnV0dG9uPicsCiAgICAgICc8YSBocmVmPSInICsgV0EgKyAnP3RleHQ9JyArIGVuY29kZVVSSUNvbXBvbmVudCgnSGksIEkgd291bGQgbGlrZSBhIHF1b3RlIGZvciBzb2xhciBjYWJsZS4nKSArICciIHRhcmdldD0iX2JsYW5rIiByZWw9Im5vb3BlbmVyIiBzdHlsZT0icGFkZGluZzoxMnB4IDIycHg7Ym9yZGVyLXJhZGl1czo2cHg7YmFja2dyb3VuZDojMTZhMzRhO2NvbG9yOiNmZmY7Zm9udC1zaXplOjE1cHg7Zm9udC13ZWlnaHQ6NjAwO3RleHQtZGVjb3JhdGlvbjpub25lIj5XaGF0c0FwcDwvYT4nLAogICAgICAnPC9kaXY+JywKICAgICAgJzxwIHN0eWxlPSJtYXJnaW46MTBweCAwIDA7Zm9udC1zaXplOjEycHg7Y29sb3I6IzY0NzQ4YiI+V2UgcmVwbHkgd2l0aGluIDIgYnVzaW5lc3MgaG91cnMgKE1vbi1TYXQsIDA4OjAwLTIwOjAwIEdNVCs4KS48L3A+JywKICAgICAgJzwvZm9ybT4nLAogICAgICAnPC9kaXY+JwogICAgXS5qb2luKCcnKTsKCiAgICB2YXIgZm9vdGVyID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignZm9vdGVyJyk7CiAgICBpZiAoZm9vdGVyICYmIGZvb3Rlci5wYXJlbnROb2RlKSB7IGZvb3Rlci5wYXJlbnROb2RlLmluc2VydEJlZm9yZShzZWN0aW9uLCBmb290ZXIpOyB9CiAgICBlbHNlIHsgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChzZWN0aW9uKTsgfQogICAgd2lyZShzZWN0aW9uLnF1ZXJ5U2VsZWN0b3IoJ2Zvcm0nKSk7CiAgfQoKICBpZiAoZG9jdW1lbnQucmVhZHlTdGF0ZSA9PT0gJ2xvYWRpbmcnKSB7CiAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgbW91bnQpOwogIH0gZWxzZSB7CiAgICBtb3VudCgpOwogIH0KfSkoKTsK"
).decode("utf-8")

OLD_ACTION_RE = re.compile(r'<form action="https://formsubmit\.co/[^"]*" method="POST">\s*'
                           r'(?:<input type="hidden" name="(?:_subject|_captcha|_template|_next|source_page)"[^>]*>\s*)*')

NEW_FORM_TAG = ('<form data-jlcc-form method="post" '
                'action="mailto:xxy13992859166@gmail.com?subject=Solar%20cable%20inquiry" '
                'enctype="text/plain">')

CTA_OLD = 'document.querySelector("form[action*=\'formsubmit.co\']")'
CTA_NEW = 'document.querySelector("form[data-jlcc-form]") || document.getElementById("contact")'

ROOT = pathlib.Path('.')


def read(p):
    return p.read_text(encoding='utf-8', errors='replace')


def main():
    js_path = ROOT / 'assets' / 'inquiry-form.js'
    before_js = read(js_path) if js_path.exists() else ''
    if before_js != NEW_JS:
        js_path.write_text(NEW_JS, encoding='utf-8')
        print('inquiry-form.js: written (%d bytes)' % len(NEW_JS.encode('utf-8')))
    else:
        print('inquiry-form.js: unchanged')

    bumped = 0
    for p in sorted(ROOT.rglob('*.html')):
        s = read(p)
        if 'inquiry-form.js?v=2' in s:
            s = s.replace('inquiry-form.js?v=2', 'inquiry-form.js?v=3')
            p.write_text(s, encoding='utf-8')
            bumped += 1
    print('cache-bust bumped: %d pages' % bumped)

    idx = ROOT / 'index.html'
    s = read(idx)
    s2, n = OLD_ACTION_RE.subn(NEW_FORM_TAG, s)
    if n == 1:
        idx.write_text(s2, encoding='utf-8')
        print('index.html: form rewritten to mailto handoff')
    elif NEW_FORM_TAG in s:
        print('index.html: already rewritten')
    else:
        sys.exit('index.html: expected 1 form rewrite, got %d' % n)

    tag = '<script src="/suncable-website/assets/inquiry-form.js?v=3" defer></script>'
    if 'inquiry-form.js' in s2:
        print('index.html: form script already present')
    elif '</body>' in s2:
        idx.write_text(s2.replace('</body>', tag + chr(10) + '</body>', 1), encoding='utf-8')
        print('index.html: form script injected')
    else:
        sys.exit('index.html: no </body> to anchor the script tag')

    cta = ROOT / 'assets' / 'sticky-cta.js'
    c = read(cta)
    if CTA_OLD in c:
        cta.write_text(c.replace(CTA_OLD, CTA_NEW), encoding='utf-8')
        print('sticky-cta.js: quote-button target updated')
    elif CTA_NEW in c:
        print('sticky-cta.js: already updated')
    else:
        sys.exit('sticky-cta.js: target selector not found')

    left = []
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.suffix in ('.html', '.js', '.json', '.xml'):
            if 'formsubmit' in read(p).lower():
                left.append(str(p))
    if left:
        sys.exit('formsubmit still referenced in: %s' % ', '.join(left))
    print('relay references remaining: 0')

    sm = ROOT / 'sitemap.xml'
    if sm.exists():
        locs = len(re.findall(r'<loc>', read(sm)))
        print('sitemap locs: %d' % locs)
    print('DONE')


if __name__ == '__main__':
    main()
