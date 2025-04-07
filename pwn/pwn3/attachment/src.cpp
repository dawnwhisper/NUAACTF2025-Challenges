#include <iostream>
#include <map>
#include <vector>
#include <string>
using namespace std;


int chance = 1;
vector<string> bandNames = {
    "Poppin'Party",
    "Afterglow",
    "Pastel Palettes",
    "Roselia",
    "Hello Happy World",
    "RAISE A SUILEN",
    "Morfonica",
    "MyGO!!!!!",
    "Ave Mujica"
};
// 99 96 12 4
map<string, vector<string>> bandMembers = {
    {"Poppin'Party", {"Kasumi Toyama", "Arisa Ichigaya", "Rimi Ushigome", "Sāya Yamabuki", "Tae Hanazono"}},
    {"Afterglow", {"Ran Mitake", "Moca Aoba", "Himari Uehara", "Tomoe Udagawa", "Tsugumi Hazawa"}},
    {"Pastel Palettes", {"Aya Maruyama", "Hina Hikawa", "Chisato Shirasagi", "Maya Yamato", "Eve Wakamiya"}},
    {"Roselia", {"Yukina Minato", "Sayo Hikawa", "Lisa Imai", "Ako Udagawa", "Rinko Shirokane"}},
    {"Hello Happy World", {"Kokoro Tsurumaki", "Kaoru Seta", "Hagumi Kitazawa", "Kanon Matsubara", "Misaki Okusawa (Michelle)"}},
    {"RAISE A SUILEN", {"Rei Wakana", "Rokka Asahi", "Masuki Sato", "Reona Nyubara", "Chiyu Tamade"}},
    {"Morfonica", {"Mashiro Kurata", "Tōko Kirigaya", "Nanami Hiromachi", "Tsukushi Futaba", "Rui Yashio"}},
    {"MyGO!!!!!", {"Tomori Takamatsu", "Anon Chihaya", "Rāna Kaname", "Soyo Nagasaki", "Taki Shina"}},
    {"Ave Mujica", {"Sakiko Togawa", "Nyamu Yutenji", "Umiri Hayashi", "Kanon Takao", "Mutsumi Wakaba"}}
};
class PopMart {
public:
    string name;
    PopMart(string name = "") : name(name) {}
    bool satisfied() {
        cout << "input a number:" << endl;
        int target = rand() % 100;
        int num;
        cin >> num;
        if (num == target) {
            cout << "You got a SSR!" << endl;
            return true;
        } else {
            cout << "You got a R!" << endl;
            return false;   
        }
    }
};
vector<PopMart*> buy_list;

vector<PopMart*>::iterator buyGoods(vector<PopMart*>& popmart_list) {
    cout << "Which one do you want to buy?" << endl;\
    string name;
    cin >> name;
    vector<PopMart*>::iterator find_SSR = vector<PopMart*>::iterator();
    for (auto it = popmart_list.begin(); it != popmart_list.end(); ) {
        PopMart* popmart = *it;
        if (popmart->name == name) {
            PopMart* newpopmart = new PopMart(bandMembers[name][rand() % 5]);
            buy_list.push_back(newpopmart);
            if (popmart->satisfied()) {
                find_SSR = std::prev(buy_list.end());
                return find_SSR;
            }
        }
        ++it;
        
    }
    return find_SSR;
}

void init() {
    cout << "Welcome to PopMart Shop!" << endl;
    cout << "try your best to get the bang SSR you like" << endl;
    buy_list.reserve(32);
}
void banner() {
    cout <<  "1. Buy goods"  << endl;
    cout <<  "2. Show goods"  << endl;
    cout <<  "3. Select"  << endl;
    cout <<  "4. Rename Your Goods" << endl;
    cout <<  "5. Exit" << endl;
    cout <<  ">> " ;
}

int main() {
    try {
        int id;
        init();
        cout << "plz input your user account:" << endl;
        cin >> id;
        srand(id);
        vector<PopMart*> popmart_list;
        vector<PopMart*>::iterator wanted = vector<PopMart*>::iterator();
        cout << "We have 9 goods for you:" << endl;

        for (int i = 0; i < 9; i++) {
            PopMart* popmart = new PopMart(bandNames[i]);
            popmart_list.push_back(popmart);
        }
        vector<PopMart*>::iterator find_SSR = vector<PopMart*>::iterator();
        while (true) {
            banner();
            int choice;
            cin >> choice;
            switch (choice) {
                case 1: {
                    find_SSR = buyGoods(popmart_list);
                    break;
                }
                case 2: {
                    cout << "Purchased goods:" << endl;
                    for (auto it = buy_list.begin(); it != buy_list.end(); it++) {
                        cout << (*it)->name << endl;
                    }
                    break;
                }
                case 3: {
                    if (chance) {
                        wanted = find_SSR;
                        chance--;
                    } else {
                        cout << "You have no chance!" << endl;
                    }
                    break;
                }
                case 4: {
                    if ((wanted) == vector<PopMart*>::iterator()) continue;
                    cout << "plz input your new name:" << endl;
                    string name;
                    cin >> name;
                    (*wanted)->name = name;
                    break;
                }
                case 5: {
                    cout << "Exiting..." << endl;
                    cout << "Haha! U can't exit!" << endl;
                    break;
                }
                default: {
                    cout << "Invalid choice!" << endl;
                    break;
                }
            }
        }
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }
}
