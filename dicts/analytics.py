import subprocess


  proc = subprocess.Popen("top -b n 1 | grep threaded_tweets.py | awk '{print $9}'", shell = True, stdout=subprocess.PIPE)
  p = proc.communicate()

  #get % CPU usage for
  p[0].decode("utf8").replace("\n","")