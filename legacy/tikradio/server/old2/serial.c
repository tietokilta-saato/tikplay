/* (c) kirma@cs.hut.fi 2003 */
/* edit nvahasar@niksula.hut.fi 2004 */

#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>

int main (int argc, char **argv)
{
      int fd;
      int status;

      int out = 0;
      int outold = 0;
      int error = 0;
            
      if (argc != 2)
	  return 1;

      fd = open(argv[1], O_RDWR | O_NOCTTY | O_NDELAY);
      if (fd == -1)
         perror("open_port: Unable to open serial port device - ");
      else
         error = fcntl(fd, F_SETFL, 0);
      
      if (error == -1)
         perror("fcntl error -  ");

      while (1) {
	  error = 0;
	  error = ioctl(fd,TIOCMGET,&status);
	  if (error == -1)
	      perror("ioctl1 GET error - ");
	  else {
	      outold = out;
	      out = 2 * ((status & TIOCM_CTS) == TIOCM_CTS) +
		  ((status & TIOCM_CD) == TIOCM_CD);


	      if (out != outold && outold == 0)
		  printf("STATUS: %d\n", out);
		  fflush(stdout);
	  }

	  usleep(100000);
      }

      /* shouldn't happen */

      close(fd);

      return 1;
}
