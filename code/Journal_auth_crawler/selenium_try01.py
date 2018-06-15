# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 00:08:00 2018

@author: Administrator
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(executable_path='C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe')
driver.get("https://www.sciencedirect.com/journal/accident-analysis-and-prevention/issues")

driver.find_elements_by_id('0-accordion-tab-0')

b = driver.find_elements(By.XPATH, '//*[@id="0-accordion-tab-0"]')
buttons = driver.find_elements(By.XPATH, '//button')
button_s = driver.find_elements_by_xpath('//button')
#buttons[6].click
webdriver.ActionChains(driver).click(button_s[6])

#chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" 
#driver2 = webdriver.Chrome(chromedriver)
#
#journal_url = 'https://www.sciencedirect.com/science/journal/00014575'
#
#driver2.get(journal_url)

<button id="0-accordion-tab-0" type="button" class="accordion-panel-title u-padding-ver-s u-text-left text-l js-accordion-panel-title" aria-expanded="true" aria-controls="0-accordion-panel-0"><span class="accordion-title js-accordion-title">2018 — Volumes 110-118</span><svg focusable="false" viewBox="0 0 92 128" width="17.25" height="24" class="icon icon-navigate-up accordion-icon navigate-up"><path d="m46 46l-38 38-7-7 45-45 45 45-7 7z"></path></svg></button><div id="0-accordion-panel-0" class="accordion-panel-content u-padding-ver-s js-accordion-panel-content" aria-labelledby="0-accordion-tab-0"><section class="js-issue-list-content"><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/118/suppl/C"><span class="anchor-text">Volume 118&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s"><span class="u-text-italic">In progress</span> (September 2018)</span></span></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/117/suppl/C"><span class="anchor-text">Volume 117&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-456 (August 2018)</span></span></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/116/suppl/C"><span class="anchor-text">Volume 116&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-126 (July 2018)</span></span><div class="js-special-issue-title">Simulation of Traffic Safety in the Era of Advances in Technologies</div></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/115/suppl/C"><span class="anchor-text">Volume 115&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-208 (June 2018)</span></span></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/114/suppl/C"><span class="anchor-text">Volume 114&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-90 (May 2018)</span></span><div class="js-special-issue-title">Road Safety on Five Continents 2016 - Conference in Rio de Janeiro, Brazil.</div></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/113/suppl/C"><span class="anchor-text">Volume 113&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-340 (April 2018)</span></span></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/112/suppl/C"><span class="anchor-text">Volume 112&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-134 (March 2018)</span></span></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/111/suppl/C"><span class="anchor-text">Volume 111&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-364 (February 2018)</span></span></div><div class="issue-item u-margin-bottom-s"><a class="anchor text-m" href="/journal/accident-analysis-and-prevention/vol/110/suppl/C"><span class="anchor-text">Volume 110&nbsp;</span></a><span class="js-issue-status"><span class="js-issue-status text-s">Pages 1-190 (January 2018)</span></span></div></section></div>
//*[@id="0-accordion-tab-0"]