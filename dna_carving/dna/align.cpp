//
//  align.cpp
//  dna_alignment
//
//  Created by Erika DeBenedictis on 1/27/13.
//  Copyright (c) 2014 California Institute of Technology. All rights reserved.
//
#include <iostream>
#include <string>
#include <unordered_map>
#include <fstream>

using namespace std;

// scoring values
#define GAP_SCORE -5
#define MISMATCH -1
#define MATCHING 2

/**
 * @brief Packages the score and instruction string the align function returns
 */
struct align_result {
    int score;      // score of this alignment
    string inst;    // instruction on how to align the inputs

    align_result(int s, string i) {
        this->score = s;
        this->inst = i;
    }
    align_result() {
        this->score = 0;
        this->inst = "";
    }
};

// memo_type will allow us to hash the string input to align
// with its output for memoization
typedef unordered_map<string, align_result> memo_type;


/**
 * @brief Function takes two strings, s and t, and produces an align_result
 * of the highest alignment score and its corresponding instruction str.
 */
align_result align(string s, string t, memo_type &memo) {
    // if this result is memoized, use recorded result
    string key = s + "," + t;
    if (memo.count(key) > 0){
      return memo[key];
    }

    if(s == "" || t == "")
    {
        align_result answer;
        int dashes = s.size() - t.size();
        string c = "s";
        if(dashes < 0)
        {
            dashes = -dashes;
            c = "t";
        }
        for(int i = 0; i < dashes; i++)
        {
            answer.score += GAP_SCORE;
            answer.inst += c;
        }
        memo[key] = answer;
        return answer;
    }

    align_result choice_1, choice_2, choice_3;

    if(s[0] == t[0])
    {
        choice_1.score += MATCHING;
        choice_1.inst += "|";
    }
    else
    {
        choice_1.score += MISMATCH;
        choice_1.inst += "*";
    }
    choice_2.score += GAP_SCORE;
    choice_3.score += GAP_SCORE;
    choice_2.inst += "s";
    choice_3.inst += "t";

    align_result choice_1r, choice_2r, choice_3r;
    choice_1r = align(s.substr(1), t.substr(1), memo);
    choice_2r = align(s.substr(1), t, memo);
    choice_3r = align(s, t.substr(1), memo);

    choice_1.score += choice_1r.score;
    choice_1.inst += choice_1r.inst;
    choice_2.score += choice_2r.score;
    choice_2.inst += choice_2r.inst;
    choice_3.score += choice_3r.score;
    choice_3.inst += choice_3r.inst;

    align_result answer;
    if(choice_1.score > choice_2.score)
        answer = choice_1;
    else
        answer = choice_2;
    if(choice_3.score > answer.score)
        answer = choice_3;
    memo[key] = answer;
    return answer;
}

/**
 * @brief Wrapper function to print the results of align
 */
void DNA_align(string s, string t) {
    cout << endl << "Calling DNA align on strings " << s << ", " << t << endl;

    // create the memoization system
    memo_type memo;

    align_result answer = align(s, t, memo);
    string ans = answer.inst;
    int score = answer.score;

    // Printing section
    // line where string s will be printed, spaces inserted
    string line1 = "";
    // line where string t will be printed, spaces inserted
    string line2 = "";
    // description of the relationship between s and t here (* | s t)
    string line3 = "";

    int j = 0;      // running index in s
    int k = 0;      // running index in t

    for (unsigned int m = 0; m < ans.length(); m++) {
        // i is the next element in our instruction string ans
        string i = ans.substr(m, 1);

        // only in s
        if(i.compare("s") == 0){
            line1 += s[j]; j++;
            line2 += " ";
            line3 += "s";
        }

        // only in t
        else if (i.compare("t") == 0){
            line1 += " ";
            line2 += t[k]; k++;
            line3 += "t";
        }

        // mismatch
        else if (i.compare("*") == 0){
            line1 += s[j]; j++;
            line2 += t[k]; k++;
            line3 += "*";
        }

        // match
        else {
            line1 += s[j]; j++;
            line2 += t[k]; k++;
            line3 += "|";
        }
    }
    cout << line1 << endl << line2 << endl << line3 << endl;
    cout << "Score for this alignment: " << score << endl;
}

int main(){
    // some test cases to begin with
    DNA_align("",   "a");
    DNA_align("b",  "");
    DNA_align("a", "a");
    DNA_align("b",  "a");
    DNA_align("b",  "ba");
    DNA_align("ab", "ba");
    DNA_align("ab", "b");
    DNA_align("abracadabra", "avada kedavra");
    string flu_a = "", line, line_2, swine_flu = "";
    ifstream file_1, file_2;
    file_1.open("Flu_A.txt");
    while(getline(file_1, line))
        flu_a += line + " ";
    flu_a = flu_a.substr(0, flu_a.size() - 1);
    file_1.close();
    file_2.open("Swine_Flu.txt");
    while(getline(file_2, line_2))
        swine_flu += line_2 + " ";
    swine_flu = swine_flu.substr(0, swine_flu.size() - 1);
    file_2.close();
    DNA_align(flu_a, swine_flu);
    /*
     * For some reason, aligning these strings does not print the proper s and t;
     * however, it prints an alignment score and instruction string which both
     * seem reasonable. I already checked that the values of both strings are correct.
     * They just do not print correctly. It prints flu_a twice instead of flu_a
     * and swine_flu.
     */
    return 0;
}
