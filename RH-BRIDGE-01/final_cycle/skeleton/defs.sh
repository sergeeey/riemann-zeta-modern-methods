#!/bin/bash
cd ~/h12/rh/src || exit 1
show() {  # regex file-line-count
  f=$(grep -rlE --include=*.lean "$1" . | head -1)
  echo "=== $1  [$f]"
  grep -nE -A${2:-6} "$1" "$f" | head -${3:-14} | cut -c1-260
}
show "^(def|abbrev|structure|theorem) (UpperTheory\.)?EveryCharacter\b" 3 6
show "^def VWin\b|^(def|abbrev) UpperTheory\.Top\.VWin\b|(def|abbrev) VWin " 4 8
show "structure UpperTheory.LiteratureTheorems.OpenLiteratureStatements" 4 6
show "(def|abbrev|structure) (UpperTheory\.)?GalStar\.Row0b|def Row0b" 4 8
show "theorem (Formalism\.VW\.)?rh_of_every\b" 3 6
show "def RiemannHypothesis|RiemannHypothesis :" 1 2
echo "=== lines 215-218 EveryCharacterOfLiteratureOfVWin"
sed -n '213,218p' Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean | cut -c1-300
