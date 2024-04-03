# Testing Boardgame Buddy
This project was tested continuously during development. Post build, the site has been manually tested by myself and third party testers. It has also passed on html, CSS, JS, and accessibility validators. 

[return to README.md](README.md)

**PLEASE NOTE: This documentation contains many images which can be viewed via a dropdown toggle.**
## Table of Contents
* [**During Development Testing**](#during-development-testing)
    * [*Manual Testing*](#manual-testing)
    * [*Bugs and Fixes*](#bugs-and-fixes)
* [**Post Development Testing**](#post-development-testing)
  * [**Post Development Testing Expanded**](#post-development-testing-expanded)
    * [Home Page Manual Testing](#home-page-manual-testing)
  * [**User Story Testing**](#user-story-testing)
  * [**Validators**](#validators)
      * [*HTML*](#html---httpsvalidatorw3orgnu)
      * [*CSS*](#css---httpsjigsaww3orgcss-validator)
      * [*JavaScript*](#javascript---httpsjshint.com)
  * [**Lighthouse Scores**](#lighthouse-scores)
  * [**Accessibility**](#accessibility)
* [**Third Party Testing**](#third-party-testing)
*  [**Third Party Feedback**](#third-party-feedback)
* [**With Thanks**](#thank-you-to-my-product-testers)

## **During Development Testing**
During the development process, I was manually testing in the following ways:-

1. Manually tested each element for appearance and responsiveness via a simulated live server by running app.py in PORT 5000.

2. 
    
3. 

## Manual Testing:

### Browser Compatibility
During testing, I used four different browsers to ensure cross-compatibility. The desktop browsers used by myself were:

  1. Chrome
  2. Firefox  
  3. Edge

Shaun Russell - Site tester - Tested on Chrome, Firefox, and Edge.
Tom Harris - Site tester - Tested the project on Safari.

### Screen Sizes

The site has been tested at screen sizes 320px to ###px in width.

<details><summary>Screen Size: 320px</summary>
<img src="">
</details>
<details><summary>Screen Size: ###px</summary>
<img src="">
</details>

### Function Testing
<details><summary>Function Testing Image</summary>
<img src="">
</details><br/>
The functions are all tested via their output displayed in the UI, the console, or both. (All console.log and console.info have been removed in the final version of the project).

[**Back to top**](#testing-boardgame-buddy)
## ***Bugs and Fixes:***

Below is a list of bugs I found during the development process by testing myself :-

1. **Deployment Issue** - 
    * ***Issue Found:*** 
        * Initial build and deployment to Heroku failed.
        * Error message: "Push failed: cannot parse Procfile"
            <details><summary>Click here to view the error image</summary>
            <img src="documents/testing-images/parse-procfile-error.png">
            </details>
    * ***Solution Used:*** 
        
2. **ISSUE NAME** 
    * ***Issue Found:***
        * ...
    * ***Solution Used:***    
        * ...
3. **ISSUE NAME** 
    * ***Issue Found:*** 
        * ...
    * ***Solution Used:***    
        * ...
4. **ISSUE NAME** 
    * ***Issue Found:*** 
        * ...
    * ***Solution Used:***    
        * ...
5. **ISSUE NAME** 
    * ***Issue Found:*** 
        * ...
    * ***Solution Used:***    
        * ...

[**Back to top**](#testing-boardgame-buddy)  
## **Post Development Testing**

Post development, I manually tested in the following ways:-

1. Manually tested each element for appearance and responsiveness via a simulated live server.

2. The code passed through HTML, CSS, JavaScript(ES6) validators to check for errors.
* [**Validators Results**](#validators)
3. The code passed through an Accessibility evaluation. 
*  [**Accessibility Results**](#accessibility)
4. Published the page via GitHub pages and shared with fellow students to test and receive feedback.

5. Sent my gitHub to link to three third party testers with different devices, browsers, and skill sets:
    - Dan Sanderson - Senior Developer
    - Shaun Russell - Senior UI/UX/Product Designer
    - Tom Harris - Enterprise Account Manager, krystal.io and Safari user 

## **Post Development Testing Expanded**

My manual testing logs are as follows:
***
### Home Page Manual Testing
***
**Home Page Test 1 -  Incorrect URL (random letter character)**
* Expected:
  * Site expected to display 404-page when the user enters an incorrect URL.
* Testing:
  * Tested site by adding a random letter at the end of URL
* Result:
  * The site acted as expected and showed its custom 404-page.
* Action: 
  * None
***
**Home Page Test 2 -  Incorrect URL (random number character)**
* Expected:
  * 
* Testing:
  * 
* Result:
  * 
* Action: 
  * 
***

[**Back to top**](#testing-boardgame-buddy)

## **User Story Testing**
1. **As a user, I want to be entertained.**
  * The site provides:
    * Entertainment in the form of a game play. 
    * User interactive elements.
    * Fast feedback to user interactions. 
    * Countdown to build suspense.
    * Rewarding Game-Over feedback with animated gifs.
    * Availability on mobile device to play anywhere, and anytime.  

[**Back to top**](#testing-boardgame-buddy)
## **Validators**

### HTML - https://...

<details><summary>HTML validator Results Image</summary>
<img src="">
</details> 

* ***Errors Found:***
    * None
* ***Warnings Found:***
    * 
* ***Action Taken:***
    * None

### CSS - https://...

<details><summary>CSS validator Results Image</summary>
<img src="">
</details> 

* ***Errors Found:***
    * None
* ***Action Taken:***
    * N/A

### JavaScript - https://jshint...

<details><summary>JS validator Results Image</summary>
<img src="">
</details> 

JSHint validator was configured to recognise New JavaScript Features (ES6), and jQuery.
* ***Errors Found:***
    * None
* ***Action Taken:***
    * N/A

## Lighthouse Scores
### Test conditions
* All lighthouse tests were run in incognito mode to avoid interference from browser extensions. 
* Both mobile and desktop performance are tested. 

<details><summary>Desktop Results</summary>
<img src="">
</details> 

<details><summary>Mobile Results</summary>
<img src="">
</details> 
<br/>

## **Accessibility** 
In addition to the accessibility score on lighthouse, [WAVE - Web accessibility evaluation tool](https://wave.webaim.org/) has been used to check the site for accessibility issues. 
<details><summary>Wave Accessibility Evaluation Results Image</summary>
<img src="">
</details> 

* ***Errors Found:***
    * None
* ***Contrast Errors Found:***
    * None
* ***Alerts Found:***
    * 
* ***Action Taken:***
    * None.
    * Reason: 

[**Back to top**](#testing-boardgame-buddy) 
### **Third Party Testing**

1. **Final result "Draw"**
    * ***Tester feedback: Shaun Russell***
        * The "Final Result: Draw" outcome is confusing to the user. 
        * Suggestion: Have "Win" and "Lose" game completion options only.
        * Draw will continuously tally until Win or Lose scores reach three.
2. **TEST NAME**
    * ***Tester...***
        *
### Third Party Feedback
1. <u>** ###EXAMPLE DO NOT LEAVE THIS IN###Dan Sanderson - Senior Developer.**</u>
  * "It looks great to me. Plays well and reliably. Nice job!".
 
  * "Some UI feedback, but it's minor, it's a bit difficult to know who's won each turn until you look closely and read the text. It's not in-your-face, but maybe that's what you're going for... One way around this might be to change the background colour of the results box to red or green if you lose or win, but I know your palette is monotone, so not sure how that would work".

  * "A future feature you could add would be to take all the hardcoded text out of your JS and HTML files and stick that in a language file. Then you can just run it through google translate or something and then have an English and maybe a French option etc which you can swap with a button."

## Thank you to my product testers
- Richard Wells: Senior Developer, and my Code Institute Mentor.

- Dan Sanderson: Senior Developer.

- Shaun Russell: Senior UI/UX/Product Designer. 

- Tom Harris: Site tester, Safari user.

- Various friends and family members.

[**Back to top**](#testing-boardgame-buddy)

[return to README.md](README.md)