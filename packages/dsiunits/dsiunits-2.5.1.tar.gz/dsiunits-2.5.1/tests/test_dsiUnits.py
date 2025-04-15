# This file is part of dsiUnits (https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import pytest
import sys
import math
import re
from itertools import combinations

from dsiUnitNode import dsiUnitNode
from dsiUnits import dsiUnit
from dsiParser import _getClosestStr, dsiParser, NonDsiUnitWarning
from regexGenerator import generateRegex
from regexGenerator import generateListRegex
from fractions import Fraction

import requests
import os

# Access the machine epsilon for the float data type
epsilon = sys.float_info.epsilon


PROXY_CANDIDATES = [
    "http://proxy:3128",
    "http://proxy:8080",
    "http://fw:8080",
    "http://firewall:8080",
    # Add your working one here directly to test!
    "http://webproxy.bs.ptb.de:8080",
]

def can_proxy_connect(proxy_url):
    try:
        proxies = {"http": proxy_url, "https": proxy_url}
        resp = requests.get("http://example.com", proxies=proxies, timeout=3)
        return resp.status_code == 200
    except Exception:
        return False

@pytest.fixture(scope="module", autouse=True)
def configure_proxy_if_needed():
    if "http_proxy" in os.environ or "HTTP_PROXY" in os.environ:
        print("✅ Proxy already configured in environment.")
        return

    for proxy_url in PROXY_CANDIDATES:
        if can_proxy_connect(proxy_url):
            for var in ["http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY"]:
                os.environ[var] = proxy_url
            print(f"✅ Proxy set from working candidate: {proxy_url}")
            return

    print("⚠️ No working proxy configured or detected.")



def test_baseCase():
    # Most basic case: one unit without prefix or exponent
    tree = dsiUnit(r'\metre')
    assert tree.tree == [[dsiUnitNode('','metre',1.0)]]
    assert tree.toLatex() == r'$$\mathrm{m}$$'
    assert tree.valid
    assert tree.warnings == []

    # One longer unit
    tree = dsiUnit(r'\milli\metre\tothe{0.5}\kilogram\per\mega\second\tothe{3}\ampere\tothe{-2}')
    assert tree.toLatex() == r'$$\frac{\sqrt{\mathrm{m}\mathrm{m}}\,\mathrm{kg}}{\mathrm{M}\mathrm{s}^{3}\,\mathrm{A}^{-2}}$$'
    assert tree.valid
    assert tree.warnings == []


def test_robustness():
    # Unknown unit
    with pytest.warns(RuntimeWarning, match='The identifier «foo» does not match any D-SI units!'):
        tree = dsiUnit(r'\foo')
        assert tree.toLatex() == r'$${\color{red}\mathrm{foo}}$$'
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == ['The identifier «foo» does not match any D-SI units!']

    # Unknown string in the middle of input
    with pytest.warns(RuntimeWarning, match=r'The identifier «mini» does not match any D-SI units! Did you mean one of these «\\milli» ?'):
        tree = dsiUnit(r'\kilo\metre\per\mini\second')
        assert tree.toLatex() == r'$$\frac{\mathrm{k}\mathrm{m}}{{\color{red}\mathrm{mini}}\,\mathrm{s}}$$'
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == ['The identifier «mini» does not match any D-SI units! Did you mean one of these «\\milli»?']

    # Base unit missing
    with pytest.warns(RuntimeWarning, match=r'This D-SI unit seems to be missing the base unit! «\\milli\\tothe\{2\}»'):
        tree = dsiUnit(r'\milli\tothe{2}')
        assert tree.toLatex() == r'$${\color{red}\mathrm{m}{\color{red}\mathrm{}}^{2}}$$'
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == ['This D-SI unit seems to be missing the base unit! «\\milli\\tothe{2}»']


def test_power():
    # power
    powerTree = dsiUnit(r'\metre\tothe{2}')
    assert powerTree.tree == [[dsiUnitNode('','metre',2.0)]]
    assert powerTree.toLatex() == r'$$\mathrm{m}^{2}$$'
    assert powerTree.valid
    assert powerTree.warnings == []
    assert dsiUnit(r'\metre\tothe{0.5}').toLatex() == r'$$\sqrt{\mathrm{m}}$$'
    assert dsiUnit(r'\metre\tothe{-2}').toLatex() == r'$$\mathrm{m}^{-2}$$'
    assert dsiUnit(r'\metre\tothe{1337}').toLatex() == r'$$\mathrm{m}^{1337}$$'

    # Non-numerical power
    with pytest.warns(RuntimeWarning, match='The exponent «foo» is not a number!'):
        abcPowerTree = dsiUnit(r'\metre\tothe{foo}')
        assert abcPowerTree.toLatex() == r'$$\mathrm{m}^{{\color{red}\mathrm{foo}}}$$'
        assert abcPowerTree.warnings == ['The exponent «foo» is not a number!']

def test_prefix():
    # D-SI prefix
    prefixTree = dsiUnit(r'\kilo\metre')
    assert prefixTree.tree == [[dsiUnitNode('kilo','metre','')]]
    assert prefixTree.toLatex() == r'$$\mathrm{k}\mathrm{m}$$'
    assert prefixTree.valid

def test_node():
    # full node
    fullNodeTree = dsiUnit(r'\kilo\metre\tothe{2}')
    assert fullNodeTree.tree == [[dsiUnitNode('kilo','metre','2')]]
    assert fullNodeTree.toLatex() == r'$$\mathrm{k}\mathrm{m}^{2}$$'
    assert fullNodeTree.valid

def test_fraction():
    fractionTree = dsiUnit(r'\mega\metre\per\second\tothe{2}')
    assert fractionTree.tree == [[dsiUnitNode('mega','metre','')],[dsiUnitNode('','second','2')]]
    assert fractionTree.toLatex() == r'$$\frac{\mathrm{M}\mathrm{m}}{\mathrm{s}^{2}}$$'
    assert fractionTree.valid

    # double fraction
    with pytest.warns(RuntimeWarning, match=r'The dsi string contains more than one \\per, does not match specs! Given string: \\metre\\per\\metre\\per\\metre'):
        tree = dsiUnit(r'\metre\per\metre\per\metre')
        assert tree.toLatex() == r'$$\mathrm{m}{\color{red}/}\mathrm{m}{\color{red}/}\mathrm{m}$$'
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == [r'The dsi string contains more than one \per, does not match specs! Given string: \metre\per\metre\per\metre']

    # empty fraction
    with pytest.warns(RuntimeWarning, match=r'The dsi string contains a \\per missing a numerator or denominator! Given string: \\per\\one'):
        tree = dsiUnit(r'\per\one')
        assert tree.toLatex() == r'$$1$$'
        assert not tree.valid
        assert len(tree.warnings) == 1

def test_empty():
    with pytest.warns(RuntimeWarning, match='Given D-SI string is empty!'):
        assert dsiUnit('').toLatex() == '$$\\textpipe\\mathrm{NULL}$$'

def test_doubleBackslash():
    with pytest.warns(RuntimeWarning, match=r"Double backslash found in string, treating as one backslash: «\\\\metre\\per\\second»"):
        assert dsiUnit(r'\\metre\per\second').toLatex() == '$$\\frac{\\mathrm{m}}{\\mathrm{s}}$$'

def test_wrappers():
    assert dsiUnit(r'\metre').toLatex(wrapper='') == r'\mathrm{m}'
    assert dsiUnit(r'\metre').toLatex(wrapper='$', prefix=r'\mathrm{Unit: }', suffix=r'\mathrm{(generated from D-SI string)}') == r'$\mathrm{Unit: }\mathrm{m}\mathrm{(generated from D-SI string)}$'
    dsiParser()._latexDefaultWrapper="&"
    assert dsiUnit(r'\metre').toLatex() == r'&\mathrm{m}&'
    dsiParser()._latexDefaultWrapper = "@"
    dsiParser()._latexDefaultPrefix = r'\mathrm{Prefix}'
    dsiParser()._latexDefaultSuffix = r'\mathrm{Suffix}'
    assert dsiUnit(r'\metre').toLatex() == r'@\mathrm{Prefix}\mathrm{m}\mathrm{Suffix}@'
    dsiParser().resetToDefaults()
    assert dsiUnit(r'\metre').toLatex() == r'$$\mathrm{m}$$'
def test_getClosestMatch():
    closestMatch = _getClosestStr(r'\kiilo')
    assert closestMatch == (['kilo'])
    closestMatch = _getClosestStr(r'\mettre')
    assert closestMatch == (['metre'])
    closestMatch = _getClosestStr(r'\ttothe')
    assert closestMatch == (['tothe'])

def test_info():
    p=dsiParser()
    infoStr, dsiVersion, dsiSchemaUrl, dsiRepositoryURL =p.info()
    #assert infoStr == "D-SI Parser Version: "+ str(dsiParser)+ "using D-SI Schema Version: "+ str(dsiParser._dsiParser__dsiVersion)+ "from: "+ str(dsiParser._dsiParser__dsiRepositoryURL)+ "using D-SI Schema: "+ str(dsiParser._dsiParser__dsiSchemaUrl)
    assert dsiVersion == dsiParser._dsiParser__dsiVersion
    assert dsiSchemaUrl == dsiParser._dsiParser__dsiSchemaUrl
    assert dsiRepositoryURL == dsiParser._dsiParser__dsiRepositoryURL

def test_fractionalPowers():
    assert dsiUnit(r'\metre\tothe{0.3333333333333333333}').toLatex(wrapper='') == r'\sqrt[3]{\mathrm{m}}'
    assert dsiUnit(r'\metre\tothe{0.666666666666666}').toLatex(wrapper='') == r'\sqrt[3]{\mathrm{m}^{2}}'

def test_baseUnitConversion():
    # Test conversion of a single derived unit to its base unit
    derivedUnitTree = dsiUnit(r'\kilo\metre')
    baseUnitTree = derivedUnitTree.toBaseUnitTree()
    assert baseUnitTree.toLatex() == r'$$1000.0\cdot\mathrm{m}$$'

    # Test conversion of a complex unit with a fraction to base units
    complexUnitTree = dsiUnit(r'\kilo\watt\hour')
    complexUnitTree2 = dsiUnit(r'\kilo\watt\hour')
    complexBaseUnitTree = complexUnitTree.toBaseUnitTree()
    reduceFractionTree = complexBaseUnitTree.reduceFraction()
    megaComplexUnitTree = dsiUnit(r'\mega\watt\hour')
    voltAmpereSeconds = dsiUnit(r'\volt\ampere\second')
    assert (complexUnitTree == complexUnitTree2) == True
    assert (complexUnitTree == 'Sting') == False
    assert math.isnan(complexUnitTree.getScaleFactor('Sting'))
    assert complexUnitTree.getBaseUnit('Sting') == None
    assert (complexBaseUnitTree == megaComplexUnitTree) == False
    assert (megaComplexUnitTree == voltAmpereSeconds) == False
    kmh = dsiUnit(r'\kilo\metre\per\hour')
    ms = dsiUnit(r'\metre\per\second')
    assert kmh.getScaleFactor(ms)-3.6<epsilon
    assert kmh.getBaseUnit(ms).toLatex() == '$$\\mathrm{m}\\,\\mathrm{s}^{-1}$$'
    ohmUnitTree = dsiUnit(r'\ohm')
    otherOhmsList = [
    dsiUnit(r'\siemens\tothe{-1}'),
    dsiUnit(r'\volt\per\ampere'),
    dsiUnit(r'\watt\ampere\tothe{-2}'),
    dsiUnit(r'\second\per\farad'),
    dsiUnit(r'\weber\per\coulomb'),
    dsiUnit(r'\volt\per\ampere'),
    dsiUnit(r'\siemens\tothe{-1}'),
    dsiUnit(r'\watt\per\ampere\tothe{2}'),
    dsiUnit(r'\volt\tothe{2}\per\watt'),
    dsiUnit(r'\second\per\farad'),
    dsiUnit(r'\henry\per\second'),
    dsiUnit(r'\weber\per\coulomb'),
    dsiUnit(r'\weber\coulomb\tothe{-1}'),
    dsiUnit(r'\joule\second\per\coulomb\tothe{2}'),
    dsiUnit(r'\kilogram\metre\tothe{2}\per\second\coulomb\tothe{2}'),
    dsiUnit(r'\joule\per\second\ampere\tothe{2}'),
    dsiUnit(r'\kilogram\metre\tothe{2}\per\second\tothe{3}\ampere\tothe{2}')]
    for otherOhm in otherOhmsList:
        try:
            scaleFactor = ohmUnitTree.getScaleFactor(otherOhm)
            commonBaseUnit = ohmUnitTree.getBaseUnit(otherOhm)
        except Exception as E:
            print(E+"WAAAAAAAAAAAAAAAAAAA")
        assert scaleFactor-1<epsilon
        assert commonBaseUnit.toLatex() == '$$\\mathrm{A}^{-2}\\,\\mathrm{kg}\\,\\mathrm{m}^{2}\\,\\mathrm{s}^{-3}$$'

def test_perAndToTheNegComp():
    kmhs=(dsiUnit(r"\kilo\metre\hour\tothe{-1}"),dsiUnit(r"\kilo\metre\per\hour"))
    mss=(dsiUnit(r"\metre\second\tothe{-1}"),dsiUnit(r"\metre\per\second"))
    scaleFactorsKMH=[]
    baseUnitsKMH=[]
    # kmh to ms
    for i in range(2):
        for j in range(2):
            scaleFactorsKMH.append(kmhs[i].getScaleFactor(mss[j]))
            baseUnitsKMH.append(kmhs[i].getBaseUnit(mss[j]))
    assert all(x==scaleFactorsKMH[0] for x in scaleFactorsKMH)
    assert all(x == baseUnitsKMH[0] for x in baseUnitsKMH)
    # ms to kmh
    scaleFactorsMS=[]
    baseUnitsMS=[]
    for i in range(2):
        for j in range(2):
            scaleFactorsMS.append(mss[i].getScaleFactor(kmhs[j]))
            baseUnitsMS.append(mss[i].getBaseUnit(kmhs[j]))
    assert all(x==scaleFactorsMS[0] for x in scaleFactorsMS)
    assert all(x == baseUnitsMS[0] for x in baseUnitsMS)
    assert scaleFactorsMS[0]-(1.0/scaleFactorsKMH[0])<epsilon

def test_str():
    assert str(dsiUnit(r'\metre')) == r'\metre'
    assert str(dsiUnit(r'\metre\tothe{2}')) == r'\metre\tothe{2}'
    assert str(dsiUnit(r'\kilo\metre\tothe{2}')) == r'\kilo\metre\tothe{2}'
    assert str(dsiUnit(r'\kilo\metre\tothe{-2}')) == r'\kilo\metre\tothe{-2}'
    assert str(dsiUnit(r'\kilo\metre\tothe{0.5}')) == r'\kilo\metre\tothe{0.5}'
    assert str(dsiUnit(r'\kilo\metre\tothe{0.333333333333333}')) == r'\kilo\metre\tothe{0.333333}'
    assert str(dsiUnit(r'\kilo\metre\tothe{0.666666666666666}')) == r'\kilo\metre\tothe{0.666667}'
    assert str(dsiUnit(r'\kilo\metre\tothe{1337}')) == r'\kilo\metre\tothe{1337}'
    assert str(dsiUnit(r'\kilo\metre\tothe{2}\per\volt')) == r'\kilo\metre\tothe{2}\per\volt'

def test_complete():
    # Test 1: Volt-Ampere to Watt conversion
    VA = dsiUnit(r"\volt\ampere")
    Watt = dsiUnit(r"\watt")
    assert abs(VA.getScaleFactor(Watt) - 1.0) < epsilon, "Scale factor for VA to Watt should be 1.0"
    assert VA.getBaseUnit(Watt).toLatex() == '$$\\mathrm{kg}\\,\\mathrm{m}^{2}\\,\\mathrm{s}^{-3}$$', "Base unit representation for power should be in kg, m^2, s^-3"

    # Expanded Test Cases for Other Units of Power Equal to Watt
    units_of_power = [
        r"\volt\tothe{2}\per\ohm",  # Volt squared per ohm
        r"\ampere\tothe{2}\ohm",  # Ampere squared times ohm
        r"\volt\ampere",  # Volt times ampere (directly equivalent to watt)
        r"\kilogram\metre\tothe{2}\per\second\tothe{3}",  # kg m^2 / s^3, directly equivalent to watt
        r"\joule\per\second",  # Directly equivalent to watt
        r"\newton\metre\per\second",  # Newton metre per second
        r"\pascal\metre\tothe{3}\per\second",  # Pascal times cubic meter per second
        r"\coulomb\volt\per\second",  # Coulomb times volt per second
        r"\farad\volt\tothe{2}\per\second",  # Farad times volt squared per second
        r"\henry\ampere\tothe{2}\per\second",  # Henry times ampere squared per second
        r"\weber\ampere\per\second",  # Weber times ampere per second
        # Equivalent through direct and indirect relationships
        # Test cases involving inverse units
        r"\siemens\volt\tothe{2}"
    ]

    # Verify each unit of power is scalably equal to Watt with complete base unit conversion
    for unit_str in units_of_power:
        otherUnit = dsiUnit(unit_str)
        assert abs(otherUnit.getScaleFactor(Watt) - 1.0) < epsilon, f"Scale factor for {unit_str} to Watt should be 1.0"
        assert otherUnit.getBaseUnit(Watt).toLatex() == '$$\\mathrm{kg}\\,\\mathrm{m}^{2}\\,\\mathrm{s}^{-3}$$', f"Base unit representation for {unit_str} should be in kg, m^2, s^-3"

def test_toUTF8():
    units_of_power = [
        (r"\volt\tothe{2}\per\ohm", "V²/Ω"),
        (r"\ampere\tothe{2}\ohm", "A²Ω"),
        (r"\volt\ampere", "VA"),
        (r"\kilogram\metre\tothe{2}\per\second\tothe{3}", "kgm²/s³"),
        (r"\joule\per\second", "J/s"),
        (r"\newton\metre\per\second", "Nm/s"),
        (r"\pascal\metre\tothe{3}\per\second", "Pam³/s"),
        (r"\coulomb\volt\per\second", "CV/s"),
        (r"\farad\volt\tothe{2}\per\second", "FV²/s"),
        (r"\henry\ampere\tothe{2}\per\second", "HA²/s"),
        (r"\weber\ampere\per\second", "WbA/s"),
        (r"\siemens\volt\tothe{2}", "SV²"),
    ]

    for unit_input, expected_output in units_of_power:
        dsiTree = dsiUnit(unit_input)
        utf8_output = dsiTree.toUTF8()
        assert utf8_output == expected_output, f"Expected {expected_output}, got {utf8_output}"


def test_toUTF8WError():
    unitStrWithError=r'\molli\metre'
    with pytest.warns(RuntimeWarning, match=r'The identifier «molli» does not match any D-SI units! Did you mean one of these «\\milli, \\mole» ?'):
        unitWError = dsiUnit(unitStrWithError)
    utf8Str=unitWError.toUTF8()
    assert utf8Str == '⚠molli⚠m'

def test_fromAscii():
    test_cases = [
        # Compact form without spaces
        # Form using ^ for exponents
        ("A^2Ω", r"\ampere\tothe{2}\ohm"),
        # Handling fractions
        ("J/s", r"\joule\per\second"),
        # More complex examples
        ("WbA/s", r"\weber\ampere\per\second"),
        ("Pam³/s", r"\pascal\metre\tothe{3}\per\second"),
        # Nested exponents and fractions
        ("FV^2/s", r"\farad\volt\tothe{2}\per\second"),
        # Negative exponents
        ("m/s^2", r"\metre\per\second\tothe{2}"),
        # Multiple units without explicit multiplication sign
        ("kgm/s^2", r"\kilogram\metre\per\second\tothe{2}"),
        ("kgm²/s³", r"\kilogram\metre\tothe{2}\per\second\tothe{3}"),
    ]

def test_percent():
    percentDsiTree=dsiUnit(r'\percent')
    assert percentDsiTree.toUTF8()=='%'
    oneDsiTree=dsiUnit(r'\one')
    assert percentDsiTree.getScaleFactor(oneDsiTree)==100 #TODO double check if this is 100 or 0.01
    assert percentDsiTree.getBaseUnit(oneDsiTree).toUTF8()=='1'

def test_multiplication():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    V=dsiUnit(r'\volt')
    A=dsiUnit(r'\ampere')
    ms=dsiUnit(r'\metre\second')
    mps=dsiUnit(r'\metre\per\second')
    multiplied=m*s
    multipliedMmps=m*mps
    multipliedMpss = mps*s
    assert multiplied==ms
    assert multipliedMpss==m
    assert dsiUnit('\\metre\\tothe{2}\\second\\tothe{-1}')==multipliedMmps

def test_division():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    ms=dsiUnit(r'\metre\second')
    mps=dsiUnit(r'\metre\per\second')
    divided=ms/s
    dividedMps=mps/s
    dividedMpss = ms/mps
    assert divided==m
    assert dividedMpss==s**2
    assert dividedMps==dsiUnit(r'\metre\second\tothe{-2}')

def test_power():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    ms=dsiUnit(r'\metre\second')
    mps=dsiUnit(r'\metre\per\second')
    powered=m**2
    poweredMps=mps**2
    poweredMpss = ms**2
    assert powered==dsiUnit(r'\metre\tothe{2}')
    assert poweredMps.getScaleFactor(dsiUnit(r'\metre\tothe{2}\per\second\tothe{2}'))==1.0
    assert poweredMpss==dsiUnit(r'\metre\tothe{2}\second\tothe{2}')

def test_ComparisonOfPerAndNotPer():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    mps=dsiUnit(r'\metre\per\second')
    mpsFromDiv=m/s
    assert mps.getScaleFactor(m/s)==1.0
    assert mps.getScaleFactor(m/s)==1.0
    assert mps==mpsFromDiv


def test_ifOnlyScaled():
    V=dsiUnit(r'\volt')
    mV = dsiUnit(r'\milli\volt')
    assert (V==mV)==False
    assert mV.getScaleFactor(V)==1000,dsiUnit(r'\volt')
    min=dsiUnit(r'\minute')
    s = dsiUnit(r'\second')
    assert (min==s)==False
    assert s.getScaleFactor(min)==60,dsiUnit(r'\second')

def test_oneMultiplication():
    one=dsiUnit(r'\one')
    m=dsiUnit(r'\metre')
    assert one*m==m
    assert m*one==m
    assert m * one*one == m
    assert m/one==m
    assert m/one/one==m

def test_onePower():
    one=dsiUnit(r'\one')
    m=dsiUnit(r'\metre')
    assert one**2==one
    assert one**0==one
    assert m**0==one
    assert m*one**1==m
    assert m*one**2==m
    assert m*one**3==m

def test_negExponentToPer():
    msToTheNegOne=dsiUnit(r'\metre\second\tothe{-1}')
    mps=dsiUnit(r'\metre\per\second')
    assert mps == msToTheNegOne.negExponentsToPer()

def test_str_bits_bytes():
    assert str(dsiUnit(r'\bit')) == r'\bit'
    assert str(dsiUnit(r'\byte')) == r'\byte'
    assert str(dsiUnit(r'\kibi\bit')) == r'\kibi\bit'
    assert str(dsiUnit(r'\kibi\byte')) == r'\kibi\byte'
    assert str(dsiUnit(r'\kibi\bit\tothe{2}')) == r'\kibi\bit\tothe{2}'
    assert str(dsiUnit(r'\kibi\byte\tothe{2}')) == r'\kibi\byte\tothe{2}'
    assert str(dsiUnit(r'\mebi\bit')) == r'\mebi\bit'
    assert str(dsiUnit(r'\mebi\byte')) == r'\mebi\byte'
    assert str(dsiUnit(r'\gibi\bit')) == r'\gibi\bit'
    assert str(dsiUnit(r'\gibi\byte')) == r'\gibi\byte'
    assert str(dsiUnit(r'\tebi\bit')) == r'\tebi\bit'
    assert str(dsiUnit(r'\tebi\byte')) == r'\tebi\byte'
    assert str(dsiUnit(r'\pebi\bit')) == r'\pebi\bit'
    assert str(dsiUnit(r'\pebi\byte')) == r'\pebi\byte'
    assert str(dsiUnit(r'\exbi\bit')) == r'\exbi\bit'
    assert str(dsiUnit(r'\exbi\byte')) == r'\exbi\byte'
    assert str(dsiUnit(r'\zebi\bit')) == r'\zebi\bit'
    assert str(dsiUnit(r'\zebi\byte')) == r'\zebi\byte'
    assert str(dsiUnit(r'\yobi\bit')) == r'\yobi\bit'
    assert str(dsiUnit(r'\yobi\byte')) == r'\yobi\byte'
    assert str(dsiUnit(r'\kibi\bit\tothe{2}\per\byte')) == r'\kibi\bit\tothe{2}\per\byte'
    assert str(dsiUnit(r'\kibi\byte\tothe{-2}')) == r'\kibi\byte\tothe{-2}'
    assert str(dsiUnit(r'\mebi\bit\tothe{0.5}')) == r'\mebi\bit\tothe{0.5}'
    assert str(dsiUnit(r'\gibi\byte\tothe{0.333333333333333}')) == r'\gibi\byte\tothe{0.333333}'
    assert str(dsiUnit(r'\tebi\bit\tothe{0.666666666666666}')) == r'\tebi\bit\tothe{0.666667}'
    assert str(dsiUnit(r'\pebi\byte\tothe{1337}')) == r'\pebi\byte\tothe{1337}'

def test_digitalUnitsScalability():
    bit=dsiUnit(r'\bit')
    byte=dsiUnit(r'\byte')
    kibiBit=dsiUnit(r'\kibi\bit')
    kibiByte=dsiUnit(r'\kibi\byte')
    mebiBit=dsiUnit(r'\mebi\bit')
    mebiByte=dsiUnit(r'\mebi\byte')
    gibiBit=dsiUnit(r'\gibi\bit')
    gibiByte=dsiUnit(r'\gibi\byte')
    tebiBit=dsiUnit(r'\tebi\bit')
    tebiByte=dsiUnit(r'\tebi\byte')
    pebiBit=dsiUnit(r'\pebi\bit')
    pebiByte=dsiUnit(r'\pebi\byte')
    exbiBit=dsiUnit(r'\exbi\bit')
    exbiByte=dsiUnit(r'\exbi\byte')
    zebiBit=dsiUnit(r'\zebi\bit')
    zebiByte=dsiUnit(r'\zebi\byte')
    yobiBit=dsiUnit(r'\yobi\bit')
    yobiByte=dsiUnit(r'\yobi\byte')
    assert bit.getScaleFactor(byte)==8
    assert kibiBit.getScaleFactor(kibiByte)==8
    assert mebiBit.getScaleFactor(mebiByte)==8
    assert gibiBit.getScaleFactor(gibiByte)==8
    assert tebiBit.getScaleFactor(tebiByte)==8
    assert pebiBit.getScaleFactor(pebiByte)==8
    assert exbiBit.getScaleFactor(exbiByte)==8
    assert zebiBit.getScaleFactor(zebiByte)==8
    assert yobiBit.getScaleFactor(yobiByte)==8
    assert bit.getScaleFactor(kibiBit)==1024
    assert bit.getScaleFactor(mebiBit)==1048576
    assert bit.getScaleFactor(gibiBit)==1073741824
    assert bit.getScaleFactor(tebiBit)==1099511627776
    assert bit.getScaleFactor(pebiBit)==1125899906842624
    assert bit.getScaleFactor(exbiBit)==1152921504606846976
    assert bit.getScaleFactor(zebiBit)==1180591620717411303424
    assert bit.getScaleFactor(yobiBit)==1208925819614629174706176
    assert byte.getScaleFactor(kibiByte)==1024
    assert byte.getScaleFactor(mebiByte)==1048576
    assert byte.getScaleFactor(gibiByte)==1073741824
    assert byte.getScaleFactor(tebiByte)==1099511627776
    assert byte.getScaleFactor(pebiByte)==1125899906842624
    assert byte.getScaleFactor(exbiByte)==1152921504606846976
    assert byte.getScaleFactor(zebiByte)==1180591620717411303424
    assert byte.getScaleFactor(yobiByte)==1208925819614629174706176
    assert kibiBit.getScaleFactor(mebiBit)==1024
    assert kibiBit.getScaleFactor(gibiBit)==1048576
    assert kibiBit.getScaleFactor(tebiBit)==1073741824
    assert kibiBit.getScaleFactor(pebiBit)==1099511627776
    assert kibiBit.getScaleFactor(exbiBit)==1125899906842624
    assert kibiBit.getScaleFactor(zebiBit)==1152921504606846976
    assert kibiBit.getScaleFactor(yobiBit)==1180591620717411303424
    assert mebiBit.getScaleFactor(kibiByte)==1/128
    assert mebiBit.getScaleFactor(kibiBit) == 1 / 1024

def test_binaryPrefixMath():
    mebiByte=dsiUnit(r'\mebi\byte')
    mebiBit = dsiUnit(r'\mebi\bit')
    gibiByte=dsiUnit(r'\gibi\byte')
    shouldBeKB=gibiByte/mebiByte
    assert str(shouldBeKB) == r'1024.0*\byte'
    shouldBe8192=gibiByte/mebiBit
    assert str(shouldBe8192.toBaseUnitTree())== r'1024.0*\bit\tothe{-1}\byte'

def test_scalability_relative_units():
    percent = dsiUnit(r'\percent')
    ppm = dsiUnit(r'\ppm')
    one = dsiUnit(r'\one')

    # Check scalability between percent and one
    assert percent.getScaleFactor(one) == 100
    assert one.getScaleFactor(percent) == 0.01

    # Check scalability between ppm and one
    assert ppm.getScaleFactor(one) == 1e6
    assert one.getScaleFactor(ppm) == 1e-6

    # Check scalability between percent and ppm
    assert percent.getScaleFactor(ppm)-1e-4<epsilon # damned 9.999999999999999e-05 != 0.0001
    assert ppm.getScaleFactor(percent) == 10000

    # Additional checks to ensure conversions are precise
    assert percent.getBaseUnit(one) == dsiUnit(r'\one')
    assert one.getBaseUnit(percent) == dsiUnit(r'\one')
    assert ppm.getBaseUnit(one) == dsiUnit(r'\one')
    assert one.getBaseUnit(ppm) == dsiUnit(r'\one')
    assert percent.getBaseUnit(ppm) == dsiUnit(r'\one')
    assert ppm.getBaseUnit(percent) == dsiUnit(r'\one')

def test_nonDsiUnit():
    with pytest.warns(NonDsiUnitWarning):
        nonDsiUnit = dsiUnit(r'|fluid ounce')
        assert nonDsiUnit.nonDsiUnit == True
        assert nonDsiUnit.tree == [[dsiUnitNode('','fluid ounce', valid=False)]]

        assert dsiUnit(r'|fluid ounce') == dsiUnit(r'|fluid ounce')

        with pytest.raises(RuntimeError):
            dsiUnit(r'|fluid ounce')**2

        with pytest.raises(RuntimeError):
            dsiUnit(r'|fluid ounce')*dsiUnit(r'|international avoirdupois ounce')

        with pytest.raises(RuntimeError):
            dsiUnit(r'|fluid ounce')/dsiUnit(r'|international avoirdupois ounce')
        assert str(nonDsiUnit)=='|fluid ounce'
        assert nonDsiUnit.toLatex()==r'$$\textpipe\mathrm{fluid ounce}$$'
        assert nonDsiUnit.toUTF8()=='|fluid ounce'
        assert nonDsiUnit==nonDsiUnit

def test_sameUnitMultiplicationWithPrefixes():
    mm=dsiUnit(r'\milli\metre')
    km=dsiUnit(r'\kilo\metre')
    cm=dsiUnit(r'\centi\metre')
    m=dsiUnit(r'\metre')
    m2=km*mm
    m3=km*m*mm
    m4=m3*mm
    assert m2==dsiUnit(r'\metre\tothe{2}')

def test_PowersWithVolumes():
    volumeFromLength=dsiUnit(r'\milli\metre\tothe{3}')
    volumeAsVolume=dsiUnit(r'\micro\litre')
    assert volumeFromLength.getScaleFactor(volumeAsVolume) == 1.0
    assert volumeFromLength.getBaseUnit(volumeAsVolume) == dsiUnit(r'\metre\tothe{3}')

def test_RegexGenerator():
    dsiRegex = generateRegex()
    assert re.match(dsiRegex, r'\milli\metre\tothe{2}')
    assert re.match(dsiRegex, r'\kilo\metre\per\second')
    assert re.match(dsiRegex, r'\metre\kilogram')
    assert not re.match(dsiRegex, r'\metre\per\second\per\gram')
    assert re.match(dsiRegex, r'|ounce')
    assert not re.match(dsiRegex, r'\ounce')
    assert not re.match(dsiRegex, r'\milli\kilogram')
    assert not re.match(dsiRegex, r'\kilo\gram')
    assert not re.match(dsiRegex, r'\deci\bel')

def test_sqrtLatex():
    sqrtM = dsiUnit(r'\metre') ** 0.5
    assert sqrtM.toLatex() == r'$$\sqrt{\mathrm{m}}$$'
    sqrt3M = dsiUnit(r'\metre') ** 0.33333333333
    assert sqrt3M.toLatex() == r'$$\sqrt[3]{\mathrm{m}}$$'
    sqrt23M = dsiUnit(r'\metre') ** 0.666666666666
    assert sqrt23M.toLatex() == r'$$\sqrt[3]{\mathrm{m}^{2}}$$'

def test_ListRegexGenerator():
    dsiRegex = generateListRegex()
    assert re.match(dsiRegex, r'\milli\metre\tothe{2}')
    assert re.match(dsiRegex, r'\milli\metre\tothe{2} \milli\metre\tothe{2}')
    assert re.match(dsiRegex, r'\kilo\metre\per\second')
    assert re.match(dsiRegex, r'\metre\kilogram')
    assert not re.match(dsiRegex, r'\metre\per\second\per\gram')
    assert not re.match(dsiRegex, r'\metre\per\second\per\gram1251\metre\per\second\per\gram')
    assert not re.match(dsiRegex, r'\metre\per\second\per\gram \metre\per\second\per\gram')
    assert re.match(dsiRegex, r'|ounce')
    assert re.match(dsiRegex, r'|ounce \metre\kilogram')
    assert not re.match(dsiRegex, r'\ounce')
    assert not re.match(dsiRegex, r'\milli\kilogram')
    assert not re.match(dsiRegex, r'\kilo\gram')
    assert not re.match(dsiRegex, r'\deci\bel')


def test_exponentMath():
    mm2=dsiUnit(r'\milli\metre\tothe{2}')
    km2=dsiUnit(r'\kilo\metre\tothe{2}')
    m2=dsiUnit(r'\metre\tothe{2}')

    assert mm2.getBaseUnit(m2) == mm2
    assert mm2.getScaleFactor(m2) == 1.0e6

    assert mm2.getBaseUnit(km2) == mm2
    assert mm2.getScaleFactor(km2) == 1.0e12

    assert m2.getBaseUnit(km2) == m2
    assert m2.getScaleFactor(km2) == 1.0e6


def test_hash():
    Hmm2=hash(dsiUnit(r'\milli\metre\tothe{2}'))
    Hkm2=hash(dsiUnit(r'\kilo\metre\tothe{2}'))
    Hm2=hash(dsiUnit(r'\metre\tothe{2}'))
    Hm2_2=hash(dsiUnit(r'\metre\tothe{2}'))
    assert hash(Hmm2) != hash(Hkm2) != hash(Hm2)
    assert hash(Hm2) == hash(Hm2_2)


def test_constructor_idempotency():
    # Create an initial dsiUnit instance from a valid D-SI string.
    unit_str = r'\metre'
    unit1 = dsiUnit(unit_str)

    # When passing a dsiUnit instance to the constructor, it should return the same instance.
    unit2 = dsiUnit(unit1)
    assert unit2 is unit1, "Constructor did not return the same instance when a dsiUnit was passed."


def test_constructor_preserves_existing_state():
    # Create an initial dsiUnit instance.
    unit_str = r'\metre'
    unit1 = dsiUnit(unit_str)

    # Set an extra attribute to check for preservation.
    unit1.extra_attribute = "unchanged"

    # Pass the instance to the constructor again.
    unit2 = dsiUnit(unit1)

    # The returned instance should be the same and preserve any already set attributes.
    assert unit2 is unit1, "Constructor did not return the same instance."
    assert hasattr(unit2, "extra_attribute"), "Extra attribute was lost on reinitialization."
    assert unit2.extra_attribute == "unchanged", "Extra attribute value was altered."

def test_toSIRP_basic():
    u = dsiUnit(r"\kilogram\metre\tothe{2}\per\second\tothe{2}")
    sirp = u.toSIRP()
    assert sirp == "kg.m2.s-2"

def test_toSIRP_prefix_scaling():
    u = dsiUnit(r"\milli\metre\tothe{2}\nano\second\tothe{-2}")
    sirp = u.toSIRP()
    assert sirp == "mm2.ns-2"

def test_toSIRP_unit_order():
    # order must be preserved
    u = dsiUnit(r"\kilogram\second\metre\tothe{2}\per\second\tothe{3}")
    sirp = u.toSIRP()
    assert sirp == "kg.s.m2.s-3"

def test_toSIRP_fractional_exponent():
    u = dsiUnit.fromDsiTree(
        dsiString="",
        dsiTree=[
            [dsiUnitNode("kilo", "metre", Fraction(3, 2))],
        ]
    )
    assert u.toSIRP() =='km3_2'
    assert dsiUnit(r'\ampere\tothe{0.5}').toSIRP()=='A1_2'
    assert dsiUnit(r'\ampere\tothe{0.6666666666666666666666}').toSIRP() == 'A2_3'

def test_toSIRP_scaled_unit_uses_prefix():
    u = dsiUnit(r"\second")
    u.scaleFactor = 1e-9  # emulate ns
    # emulate that the exponent is still integer
    u.tree[0][0].exponent = 1
    sirp = u.toSIRP()
    assert sirp == "ns"

def test_toSIRP_scaled_unit_invalid_scale():
    u = dsiUnit(r"\second")
    u.scaleFactor = 3.14  # no matching SI prefix
    with pytest.raises(NotImplementedError, match="Unsupported scale factor for SI RP: 3.14"):
        u.toSIRP()

def test_toSIRP_composite_watt_units():
    units_of_power_sirp = {
        r"\volt\tothe{2}\per\ohm": "V2.Ω-1",
        r"\ampere\tothe{2}\ohm": "A2.Ω",
        r"\volt\ampere": "V.A",
        r"\kilogram\metre\tothe{2}\per\second\tothe{3}": "kg.m2.s-3",
        r"\joule\per\second": "J.s-1",
        r"\newton\metre\per\second": "N.m.s-1",
        r"\pascal\metre\tothe{3}\per\second": "Pa.m3.s-1",
        r"\coulomb\volt\per\second": "C.V.s-1",
        r"\farad\volt\tothe{2}\per\second": "F.V2.s-1",
        r"\henry\ampere\tothe{2}\per\second": "H.A2.s-1",
        r"\weber\ampere\per\second": "Wb.A.s-1",
        r"\siemens\volt\tothe{2}": "S.V2",
    }
    for expr, expected_sirp in units_of_power_sirp.items():
        u = dsiUnit(expr)
        assert u.toSIRP() == expected_sirp, f"{expr} -> {u.toSIRP()} != {expected_sirp}"




def test_bipmRp_basic():
    u = dsiUnit("kg.mm2.ns-2.℃")
    assert u.valid
    assert u.nonDsiUnit is False
    assert str(u) == r"\kilogram\milli\metre\tothe{2}\nano\second\tothe{-2}\degreecelsius"

    t = u.tree[0]
    assert t[0].prefix == ""
    assert t[0].unit == "kilogram"
    assert t[0].exponent == 1

    assert t[1].prefix == "milli"
    assert t[1].unit == "metre"
    assert t[1].exponent == 2

    assert t[2].prefix == "nano"
    assert t[2].unit == "second"
    assert t[2].exponent == -2

    assert t[3].prefix == ""
    assert t[3].unit == "degreecelsius"
    assert t[3].exponent == 1


def test_bipmRp_implicit_exponents():
    u = dsiUnit("mol.cd.m")
    assert u.valid
    assert [n.unit for n in u.tree[0]] == ["mole", "candela", "metre"]
    assert [n.exponent for n in u.tree[0]] == [1, 1, 1]


def test_bipmRp_with_explicit_and_negative_exponents():
    u = dsiUnit("kg2.m-1.s3")
    t = u.tree[0]
    assert t[0].unit == "kilogram" and t[0].exponent == 2
    assert t[1].unit == "metre" and t[1].exponent == -1
    assert t[2].unit == "second" and t[2].exponent == 3


def test_bipmRp_utf8_prefix_and_units():
    u = dsiUnit("µF.GΩ")
    assert u.valid
    assert [n.prefix for n in u.tree[0]] == ["micro", "giga"]
    assert [n.unit for n in u.tree[0]] == ["farad", "ohm"]


def test_bipmRp_invalid_unit_warns():
    u = dsiUnit("kg.xunit")
    assert not u.valid
    assert u.nonDsiUnit
    assert len(u.warnings) > 0
    assert "Unknown unit" in u.warnings[0]


def test_bipmRp_malformed_components():
    u = dsiUnit("kg..s")  # double dot
    assert not u.valid
    assert u.nonDsiUnit
    assert any("Invalid BIPM-RP component" in w for w in u.warnings)


def test_bipmRp_parse_equals_dsi():
    a = dsiUnit("kg.mm2.ns-2.℃")
    b = dsiUnit(r"\kilogram\milli\metre\tothe{2}\nano\second\tothe{-2}\degreecelsius")
    assert a == b


def test_bipmRp_fractional_underscore_parsing():
    """
    Test that a BIPM‐RP string with fractional exponents in underscore notation is
    correctly parsed into dsiUnitNodes with Fraction exponents.

    Input: "kg.mm1_2.ns-2.℃"
        - "kg" should be recognized as kilogram with exponent 1.
        - "mm1_2" should be parsed as milli + metre with exponent Fraction(1, 2).
        - "ns-2" should be parsed as nano + second with exponent -2.
        - "℃" should be parsed as degreecelsius with an implicit exponent of 1.
    """
    u = dsiUnit("kg.mm1_2.ns-2.℃")
    assert u.valid, "Unit should be valid."
    # There should be four components in the parsed tree.
    assert len(u.tree[0]) == 4, "Expected four components in the unit tree."

    # Component 0: "kg"
    node0 = u.tree[0][0]
    assert node0.unit == "kilogram", "First component should be 'kilogram'."
    assert node0.exponent == Fraction(1), "First component exponent should be 1."

    # Component 1: "mm1_2"
    node1 = u.tree[0][1]
    assert node1.prefix == "milli", "Second component should have prefix 'milli'."
    assert node1.unit == "metre", "Second component should be 'metre'."
    assert node1.exponent == Fraction(1, 2), "Second component exponent should be 1/2."

    # Component 2: "ns-2"
    node2 = u.tree[0][2]
    assert node2.prefix == "nano", "Third component should have prefix 'nano'."
    assert node2.unit == "second", "Third component should be 'second'."
    assert node2.exponent == Fraction(-2), "Third component exponent should be -2."

    # Component 3: "℃"
    node3 = u.tree[0][3]
    # Assuming the mapping converts ℃ to 'degreecelsius'
    assert node3.unit == "degreecelsius", "Fourth component should be 'degreecelsius'."
    assert node3.exponent == Fraction(1), "Fourth component exponent should be 1."


def test_bipmRp_toSIRP_with_fractional_exponent():
    """
    Test that conversion to BIPM‐SI‐RP (toSIRP method) properly renders fractional exponents
    using underscore notation.

    Examples:
        - \metre\tothe{0.5} should yield "m1_2"
        - \ampere\tothe{0.6666666666666666} should yield "A2_3"
    """
    u = dsiUnit(r'\metre\tothe{0.5}')
    sirp_output = u.toSIRP()
    assert sirp_output == 'm1_2', f"Expected toSIRP() to return 'm1_2', but got '{sirp_output}'."

    u2 = dsiUnit(r'\ampere\tothe{0.6666666666666666}')
    sirp_output2 = u2.toSIRP()
    assert sirp_output2 == 'A2_3', f"Expected toSIRP() to return 'A2_3', but got '{sirp_output2}'."


def test_bipmRp_malformed_fraction_underscore():
    """
    Test that a malformed fractional exponent using an unexpected underscore format
    (e.g. "m1_2_3") renders the unit invalid and produces an appropriate warning.
    """
    u = dsiUnit("m1_2_3")
    assert not u.valid, "Unit should be invalid due to malformed fractional exponent."
    assert any("Invalid BIPM-RP component" in warning for warning in u.warnings), \
        "Expected a warning about Invalid BIPM-RP component"

def normalize_dsi_tree_to_tuples(unit: dsiUnit):
    """
    Normalize a dsiUnit instance into a list of (prefix, unit, exponent) tuples.
    The list will be flattened and _removePer will be applied to ensure compatibility.
    """
    import copy
    unit_copy = copy.deepcopy(unit)
    unit_copy._removePer()
    result = []
    for node in unit_copy.tree[0]:
        result.append((node.prefix or "", node.unit, int(node.exponent)))
    return result

def normalize_label(label: str) -> str:
    """Normalize unit and prefix labels for consistent comparison."""
    return label.replace(" ", "").lower()


def test_bipm_pid_json_vs_dsiUnit_instances():
    """
    Validate that the BIPM PID JSON response matches the internal dsiUnit representation.

    Also verify that invalid D-SI expressions result in a 404 when querying the PID URL.
    """
    # ✅ Valid unit expressions and their expected normalized trees
    valid_units = [
        r"\kilogram\milli\metre\tothe{2}\nano\second\tothe{-2}",
        r"\kilogram\milli\metre\tothe{2}\nano\second\tothe{-2}\astronomicalunit\tothe{-4}\degreecelsius\micro\henry",
        r"\volt\tothe{2}\per\ohm",
        r"\ampere\tothe{2}\ohm",
        r"\joule\per\second",
        r"\pascal\metre\tothe{3}\per\second",
        r"\weber\ampere\per\second",
        r"\degreecelsius",
        r"\nano\second",
        r"\micro\henry"
    ]

    for i,expr in enumerate(valid_units):
        unit = dsiUnit(expr)
        url = unit.toSIRP(pid=True)
        response = requests.get(url, timeout=10)
        assert response.status_code == 200, f"Expected 200 {url}, got {response.status_code}"

        json_data = response.json()
        try:
            bipm_units = json_data["resultsCombinedUnitList"]
        except KeyError:
            if len(unit.tree)!=1:
                raise RuntimeError("Expected taht we stated with a tree with just one entry sinc we did'nt get a combined unit back ...")
            #lets fake an ordinary response for the simple base unit ...
            bipm_units = [{'unitName':json_data['unitId'],'exponent':1,'prefixName':''}]

        parsed_bipm = []
        for item in bipm_units:
            prefix = normalize_label(item.get("prefixName", ""))
            unit_name = normalize_label(item["unitName"])
            exponent = int(item["exponent"])
            parsed_bipm.append((prefix, unit_name, exponent))

        local_tree = normalize_dsi_tree_to_tuples(unit)
        assert parsed_bipm == local_tree, f"\nExpression: {unit.dsiString}\nExpected: {local_tree}\nGot: {parsed_bipm}"

def test_bipm_pid_json_vs_dsiUnit_Invalide_instances():
    # ❌ Invalid unit expressions (syntactically wrong or non-existent)
    invalid_units = [
        dsiUnit(r"\molli\metre"),
        dsiUnit(r"\kilogram\milli\metre\tothe{2}\nano\sec\tothe{-2}"),  # typo in unit
        dsiUnit(r"\none"),
        dsiUnit(r"")
    ]

    for unit in invalid_units:
        url = unit.toSIRP(pid=True)
        response = requests.get(url, timeout=10)
        assert response.status_code == 400, f"Expected 400 for invalid PID: {unit.dsiString} → {url} but got {response.status_code}"