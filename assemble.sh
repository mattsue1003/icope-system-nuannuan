#!/bin/zsh
# parts/ → deck.html（Artifact 用）→ index.html（GitHub Pages／離線用）
cd "${0:A:h}"
python3 order.py
{
 cat parts/base/head.html parts/extra.css
 print -r -- '</style>'
 print -r -- '<div class="deck" id="deck">'
 cat parts/deck_order.html
 print -r -- '</div>'
 cat parts/base/shell.html
 print -r -- '<script>'
 print -r -- '(function(){'
 print -r -- '"use strict";'
 print -r -- 'var THR={ab:10,iv:50,pt:30};'
 print -r -- 'function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]})}'
 cat parts/base/tip.js parts/calc.js parts/base/engine.js
} > deck.html
zsh build.sh
