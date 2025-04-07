#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

using namespace std;

#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"

int main() {
    printf("Welcome to Runner!\n");
    pid_t pid = fork();
    
    if (pid < 0) {
        cerr << ANSI_COLOR_RED << "Fork error." << ANSI_COLOR_RESET << endl;
        return 1;
    }
    if (pid == 0) {
        execl("./attachment", "attachment", (char*)NULL);
        perror("exec error");
        exit(1);
    }
    int status = 0;
    waitpid(pid, &status, 0);

    if (WIFEXITED(status) && WEXITSTATUS(status) == 0) {
        cout << ANSI_COLOR_GREEN "./attachment exited normally." ANSI_COLOR_RESET << endl;
    } else {
        ifstream flagFile("flag");
        if (!flagFile) {
            cerr << ANSI_COLOR_RED << "Cannot open flag.txt"<< ANSI_COLOR_RESET << endl;
            return 1;
        }
        stringstream buffer;
        buffer << flagFile.rdbuf();
        cout << ANSI_COLOR_RED << "You escaped the shop!" << ANSI_COLOR_RESET << endl;
        cout << ANSI_COLOR_YELLOW << "ASan detected an error! Here is your flag:" << ANSI_COLOR_RESET << endl;
        cout << ANSI_COLOR_GREEN << buffer.str() << ANSI_COLOR_RESET;
    }
    return 0;
}