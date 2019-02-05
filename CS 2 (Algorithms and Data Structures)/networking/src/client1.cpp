/**
@file
@author Ben Yuan
@date 2013
@copyright 2-clause BSD; see License section

@brief
A more complex echo client to validate the network wrapper.

@section License

Copyright (c) 2012-2013 California Institute of Technology.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the California Institute of Technology.

*/

#include "client1.hpp"

using namespace CS2Net;

void send_mess(CS2Net::Socket *sock);
void receive(CS2Net::Socket *sock);

int main(int argc, char ** argv)
{

    REQUIRE(argc == 3, "usage: %s hostname port", argv[0]);
    CS2Net::Socket *sock = new CS2Net::Socket;
    string hostname(argv[1]);
    int port = atoi(argv[2]);
    int ret = sock->Connect(&hostname, port);
    if(ret < 0)
    {
        if(ret == -1)
        {
            ERROR("connect error: %s", strerror(errno));
        }
        else if(ret == -3)
        {
            ERROR("connect error: %s", gai_strerror(errno));
        }
        else
        {
            ERROR("this error should never occur");
        }
    }
    else
    {
        int pid = fork();

        if(pid > 0)
        {
            receive(sock);
        }
        else
        {
            time_t now = time(nullptr), previous = time(nullptr);
            while(true)
            {
                time(&now);
                if(difftime(now, previous) >= 1)
                {
                    send_mess(sock);
                    previous = now;
                }
            }
        }
    }

    return 0;
}

void send_mess(CS2Net::Socket *sock)
{
    string message("*munch*");
    int ret_1 = 0;
    ret_1 = sock->Send(&message);
    if(ret_1 < 0)
    {
        if(ret_1 == -1)
        {
            ERROR("send error: %s", strerror(errno));
        }
        else
        {
            ERROR("this error should never occur");
        }
    }

}

void receive(CS2Net::Socket *sock)
{
    string * incoming;
    while(true)
    {
        incoming = sock->Recv(1024, false);
        if(incoming == NULL)
        {
            ERROR("recv error: %s", strerror(errno));
        }
        else
        {
          cout << "Received: " << *incoming << endl;
        }
    }
}
