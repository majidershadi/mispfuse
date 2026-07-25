# Shared code for the mispfusepush command and the push alert action.
# Neither entry point does much on its own: they hand this package a session
# key, some options and the result rows, and let it do the real work.

APP_NAME = "mispfuse"
REST_ROOT = "mispfuse"
