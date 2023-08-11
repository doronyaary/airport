import sys,os,logging,click,json,subprocess,time,datetime,schedule,threading,psutil
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

SYS_IMG="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAAB3RJTUUH4gQaCCQDO47gtgAAJfhJREFUeNrtnXmAHFW1/z+nJiELiGyC4sYS/KHEJwQe4vLT+CRLr4FAwg4JSwigj01BFiUsT0AQcclkQgIJayBhy3RP9yQhJMgiooii4mN5iPpUBARkSyCZOu+Pmk46k0mme/pWV/X0+fxTPbeqT917p+733jp977mC0VTojBnwh8c/DnxKVT4EDAXeQ3kR+IMw5HlZtEijzqdRHyTqDBj1QQ/P7g86BSUDfARAtezfr+uOLwJ5YL7IkIdl0aKos26EiAnAAEaPzA5DdTLKacC/B4ll53sXgPK03wIzFW5tuav9rajLY7jHBGAAokdmdwOdjjIV2CFILJ0su65vASjxL5SbgFbv7vb/jrp8hjtMAAYIenTWQ3Vcd2+fALxeG3P/BKD0WVHuB1rFk3a5a/HaqMtt1IYJQIOjR2e2QzkemA7s3kcDrlUAytP+gjIHYY53T/uLUdeD0T9MABoUPSazH8qpwOHAsH404FoFoPT5PeAulFmyxZAHzWnYWJgANBB6bHYoqocBpwL7V9hAN3nekQCUf/4NSquq3tqSy70ddX0ZfWMC0ADocdldUZ0OHI92O/WgPw00bAHoPsq/gPnALK998dNR15+xaUwAYooel/CgZRzIqShJwAtOlF/Uy+d4CEDpswLLgVbxyUmHOQ3jhglAzNAp6e2g26mn7A7Sd6Mr/xwvASg//xfgOuA6L7/4pUgq19gIE4CYoFPT+wGnot1OPVjfmAaGAJSO7wF3Aq3SsfhhewCjxeo/QvSETODU026nHvTSaAacAJSn/RpoVZVbW4r3vhNeTRubwgQgAvSE9K4ogVMPdth8oxrQAlDidWA+aJtXaDenYR0xAagTOi3h4beM6+7tA6deRY2qKQRgXY6A+4BW8fyc5PNdtda7sXlMAEJGT0ptB3J8d4+/e/WNqqkEoPyPPwNtoNd7hZw5DUPCBCAkdFoPp97mGoAJwKYSAH2XktOwkHvEHli3WH06RKdn1s/U0x5OPROAzX+/94SeaU8ArQq3tRRy5jR0gAmAA/SUMqeebmL5rQnA5r/fe8Km0l4jmGnY5hXyz2D0GxOAfqKnpDxE1jv1tMdMPROAMAWg9MGn5DTEz0uhYE7DKjEBqBI9Nb09wtSNnHrVHvtKW/c5dAHwqfgXiUrP100AytNeQJmN6lyvs/AKRkWYAFSIfq0Pp17jCcAvVKVVlHsV0gQrDD/XwAJQSn4XWAjM8oodP8PYLCYAm0G/nhwC3mEEUXY279RrDAFYhXIH0Cp35H7Rs7z+pOyo7leaI4DhDSoA5Wm/AloVXdBSLJrTsBdMAHpBT0/vgjId5QSo0KkXbwF4HqUNZJ7c3t7n8NiflN0WZSrKKcCIyvNK3ASg9OE1YB4wyysWnuur/M2ECUA3embaw2cscBpKAmgJTpQucHzsK23d534LgI/SCbQiXUW5reBXXScTJ3oqa8cQvPqkgJYGFYD1dYIuBWYKFKVYbHqnYdMLgJ6Z3hZdt/x2xPoTIR/7Slv3uWoB+CdwA9Amt+Wed1VP/sTsLsDJ3aOiD2y+LLEVgPK0F4A24HqvWGxap2HTCoCeld533fuuli+/LV0Q8rGvtHWfKxaAXwCtIHfIre2rQqu3CZkh6slk4BSUz/VeloYQgBLvgt4BzPKKnY+GVW9xpakEQL+RHIJ6h3W/2x5QVeOMpwCsBu4AZsotGzv1wsY/KDuK4JXpCHrGMKi2rL0nVJdWu73HgVYVWdBSKIYmonGiKQRAv5HeBcqcev1pnPESgD8CbSA3yM19O/XCxp+Q3RbKX6MaVgBKvAZ6PdDmFZf8T10qMSIGrADomWmPQT2cerU0zugFwAeWoLQCBbk5V7VTL2w0m/UUxoIEm5NotyO1krL2nlBdmmt7pTqHVunSgixdGrs6r5UBJwB6bqrMqSe9/4TVUALAq6gETr2bcg3TG/nZCbsQzJbsfdTV83PvCdWluReAcv4I2gbc4BWXRj7qcsWAEQD9VqoXp16PoWhjCcAvUVrx9Xa5uaNh30d1wsFD1Pc39rv0LHfvCdWlhSsApbSS36XVKy59LPQKDJmGFgD9VnIIIpO7G34vTr2GE4DVlGbqzc83/MPVEz89Yb1Il0+n3qhC+plWHwEo55fATFG9QzqXNaRIN6QA6PmpzQ8vG08AAqeecIPckB8ww8tN4acmbAucQGlB1UYVUk6sBaCU1j33Qtq84lJncy/qQcMIgM7IeqzpGsv63W8rcOrFWgB8lKXATDwtytyOppuVpqlDPNW146AUJ1G9Xq6i4rToBKCED3SCtor4RSncH3unYewFQC9MBT8xBb1FlU69WArAa8ANCG0yN2/z0rvxkxN2BV0fKXkdDSUA5WnPE8w0nOcV74vtqC62AqDfTu1LMAe9xySTao6xEoDHgVZggczNN+T7Yj3QVHaoKus3QG1cASixbgWm13lf3Sdr9UWsBEBnpIbgM5mg4R8QJJZfUO0xcgF4F2Uh0Cpz8k03zbRW/GR2P9D1W6Cvo6EEoPtPBXgMaBXx75DiitXh12DfxEIAdEaZU29TMfV6S4uvALyABiGt5bqO2A7/GgU/mVm/XyLs3sACUOIVuhdseZ3L/xh2/W2OyARAZ2Q9pMypp30sv93cuXgIgA8sRZkJLUWZvbjpnHpho+OynrbouO5Rwfodk4OzjSQAJXzQAjBL/EGdUcw0rLsA6CU9nHqhNsq6CMBrdAebkFnm1KsXfjK9G8GIYCqwQ4MKQHn6/wBtiM7ziiv+GXoFdlM3AdBLU3sDXyeIqTe8Pr1yqAIQOPVUbpdZFqM+KjSZHqZwGOhpKPv1ONvbN+qfVpkAlFgFejvwQ69zxW/Crb06CIBelvoEcBVKBpB+v1v35zvuBWB1t1Nvlsw0p17c8BOp/YHTgMnA0AYVgPIv5IBvep0rQtv7IDQB0BmjYfCWp6NcTlhRdOsnAC+gzAaul5/kXw6rzgw3+InU9sAJoCcDu214tmEEoMRq4HwZvNW1ksttyki/CUUA9LvpwaheDxzj6Oe0fn63JgEoOfVaUemQn8Rv+a2xeXRsxtOWrgTBnILxgNeAAlBKu0XQ46XzgTUu68i5AOh3Ey3g3Y5y6AZlaRwBCJx6qm3yo45nXdePEQ1+IrkbcAroFDaYaQgNIgAAd4nHYVJY6ewXphAEIHU1cLazhl8/AXgCZSYiC+Rac+oNVDSZHKbBBq5fA/btTu3tSndp7gQA4Bqvc+XZrurDqQDod1PjgQK1OPvqKwDrdpHhB/mfxWJWlFE3/ESi22mok9hgpiHEWAAUSHmdK4su6sDZM69XpIbi8wdglw3yG08B+BPBQo0b5Jr8S67qwGhM/MT4HVg/03DXIDW2AgDwgqCflM4Hap5O7NVqoCx/05Duxh9PSvHdDkL93eWa/BXW+A0Ar9j5ilfs/J6IN4Jgn8ROguclruyiyDQXhpyMAPS7CUG854DdnPf8tY8AXkOZB8yWq20veaMy/MS43YFTgCnA9kFqbEYAAM+Lv8UIWbq0pp8G3QjA5akvAA9tkM/oBeAJVFpBbpOrzKln9A9NjB+m6OEEvoJ9e7mCPtPCEQBAv+B1PvBILeUb5KieEo7s1Mq7wJ1AK9/reMScekatSLFzFcFaj3l+YmxppuFhwJCo8waSAGIhAJ+NuCb+BFwHzJUrO+y93giF7ijAj/mJsWcTxKOcDpH6vWpud24EQPgENb2J9AsF7iNYkJOTK/O2/NaoC937Alyp48dfpdKVJJhpOA6XTvXK+EStBtwIgLJjHQv9OjAfaJXLbaaeER3S2ekDeSDvJ8aMYP3y5O3qlIWa250rJ6C/zlZ4TsBfo/wEYYFc1mFOPSOWaGLMMEWPJPgFIXAahuYERL3OlTWNOtwIwBUpDanhv4d2O/Uu63jYnHpGI+EnDvwswd6Uk0CH9n5VTQKA17mypmbhygnomj8Ds1HmymXm1DMaE69438+Bn/vjx5wFGgen4UbEcwTg6SCZUTCnnjGg0OSYFvX9tT1Se7uywrTaRwD19lpWhDV+YyAihWWxe65jKQCGYdQHEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiTEBMIwmxgTAMJoYEwDDaGJMAAyjiRkUdQYMoxZ03DiPlkFbIbwrHR3vRp2fRsMEwGg4/GR6N+AEIKHwKWAIqviJ1N+Ah4DbBb9disWuqPMad+wVwGgY/GRqaz+Z+RHwNHA+sA8wpOySnYHJwN2K96SfSH4x6jzHHRMAoyHwk5kx4P0W+DqVjVw/BazwE8npUec9zpgAGLHGT2a29pOZ64AlwMeq/PogoNVPJI+JuhxxxQTAiC1+MjsW+C1wEiD9NCNAm59I7h51eeKIOQGN2OEnM1uDXA2cSP8bfjnDgSuASVGXLW7YCMCIFUGvL7+jtl6/Nw72E8mPRF2+uGEjACMW+MnM+0G+DxyP24ZfogVIAbOjLmucMAEwIsdPTkgA14GG3UOPirqsccMEwIgMPzlhG+AaYGqdbvnBqMscN0wAjEjwUxOSKLOBer6X+1GXO26YABh1xU9O2Aapa69fzv9GXf64YQJg1A0/PSGF0kZ9e/1yHou6DuKGCYAROn5qwrbdvf6UCLPxLtARdV3EDRMAI1T8zIRMd6+/c8RZmecVC69GXR9xwwTACAU/e9B2qF4LHIMAGml2Xkb1oqjrJI6YABjO8bMTsqBtwIeizgvB0P8wr7P4UtQZiSMmAIYz/Gx2O+CHwNFR56Wb14HDvWJhRdQZiSu2FsBwgj8hm0X4HfFp/CtQ9vGKhSVRZyTO2AjAATo9sz3oLsAQVF4FnpfZufeizlc98A+asD2qPwDisub+LeBcwZ8lncVoPQ8NgAlAP9FTU9uDnIJyBOgn0dICFgV4R6el7wfm0LUmJ9cvGZAPon9Q9mDQWQg7RezkK7EcONErdrwQdUYaBXsF6Ad6Wvo4kGeASwlCT/VcvTYcSAOL8QY/pCelR0SdZ5f4Eyfs4B+cvQ24G9gp6vwAbwKnytAtxljjrw4bAVSBzpgEL6/6PnBWFV/7PPCYnpROyZz8z6IuQ634B2cnotpKPBo+lHr9gjX8/mAjgGp4ZdUFVNf4S2yL0qEnpveMugj9xZ+Y3cGfmF0A3EU8Gn/Q63etGeMV8i9EnZlGxQSgQvRr6f2Ai2swsS1wj56Y2jrqslSLPzE7Efg9cHjUeelmGfBpr5CfJUsGpn+lXpgAVM7lBFFlamFPVG7UYw8OI+KNc/xDsh/wD8kuQLgL2DHq/ABvACfLIG+cV8j/KerMDATMB1AB+rX0COCrjswdxOA1FwCXRV2uzeEfmp2EMhP4QNR56WYpykleMffnqDMykLARQGWMx22cuov1hHQy6kL1hn9o9gP+odmFwELi0fjfAKbJO0PHW+N3jwlAZXzasT0PuFWPj9fPg/6k7GSCd/24hM9egvJpr5CbIysX2bt+CJgAVMYOIdjcBrhbp6a2irpw/qTsjv6k7CLgDuLR6/8LOEnWrk5Yrx8uJgCVEda03k8jcr1Oy0TmFPQnZycDvwMOjSoPPSgCn/YK7XNl6VLr9UPGnICV8UKItiezRn8JXFXPAvmTszsCrcAhMVivD8HKvbNE18yTYjHqvDQNNgKojIdDtn+5Tk0fWI+CKKCHZY4Q0aeAQ+pxzwooEPT61vjrjAlAReh9wCsh3qAFuF2npncJtRSHZz7IYZl7gNuA7cO8V4W8DhwvW26R8gqLLWJvBJgAVID8pGM18IOQb7M9cLdOyQxzbVgBPTxzJMG7/kEhl6NSCsBIr7B4nixaFHVemhYTgIqRawgaUJjsA3qdTnL3K5wekfkgh2fuAW4lPr3+VHn7XymvsPivUWem2TEBqBD5SW41yqEEP1GFydFsueo/azWiM2agR3T3+hKbXj+HyF5ex+L5snJl1HkxMAGoCpmZf5og8k3YW0x9X6ekv9zfL+uR2Q/yzONx6vVfBY6VYVtkvfy9f4s6M8Z6TACqRGbmc9S2KrASBgEL9bh0VTvo6OjR6JGZY0F/T3ze9XPASC+/+GZ7148fJgD9YZB3KXBvyHfZEbhLj00PqeRiPSqzMx9+Xw64Edgu2goCSr3+0C2yXm7x36POjNE7JgD9QH7YrsCxwFMh32p/hNbNXaCjR6NHZY4lcFCmo66bbtqBkV7Oev24YwLQT6Q1/ybKwQRe7TDvdLwel5ne2xk9OrMzH3lfDuFGgoAjUfMqcIyM2meC1269fiNgAlADMiv/DPVwCio/1GMzn1/357Rp6DGx6/XvAfby2ttvkRkzos6LUSG2FqBGZFY+r9PTFxFECA6LLYBFemxmPxRh1d+vA1JRl72bV4D/lMXtCxoizJGxASYALliz5r8YPHgUcHCId9kZWAp8hGApcRy4G+VUb3H7P6LOiNE/7BXAAcHGH3IcQTCNMBlJPBr/K8CR3r3th1jjb2xMABwhbbk3oR5Owci5Gxjp3dO+IOqMGLXjRgAcryWPfml6/5C2/LPAUYQ/UzAKXgGO8O5pP8S7x3r9/qAxdI66GgG4feC/lWrYkYnMzheAb0edD8csQhjp3d1+e9QZaWgeur/WsPI96arVgCsn4FoCT7UbBnstNHIv6unldMko4hNwo7+8DJzm3dVus3lcIENaHD/WNQuAq552rctS4ak7MYkAmdWhiEwh/OXDYbIIYS9r/A5pcf5c19zu3AiAsNppsVSHO7UXATI79xaBU/C1qPNSJS8Bk7w72yd7d7a/HHVmBhTi/LleVasBV07Ad5wWS9jSqb2IkOvyzwFH4mCoVicWIuzl3dl+Z9QZGYioOn+ua253rl4B3nZaLOX9Tu1FiMzJdwIXRp2PPgh6/UXth3mL2sOMfdjsuH6uYyMArqPkxGFhizu6vCuBuL5LLwD28hZZr18HXD/Xr9dqwJUAuH7PDWMnnsiQG9oVkanAb6POSxkvAgd7C9uP9BZar18nXD/XNbe7uArATo7tRY7Myb1N4BR8Neq8EIQFH+ktbL836ow0Ga6f65qfJVcC4Hpm2M6O7cUCmZv/H6J1Cr4IHCx35I6SO3L/jLo+mhDXz/VLtRqIqwB81LG92CDX55cAF0Rw69uAveSO3L1R10ET4/q5rrnduZoJ6Dr6y8cc24sXbwz7Hu9btQ9wWB3u9iIwXW7PLY662AYfd2yv5nbnagTwF8cFG+HYXqyQRYsU5QTgyZBvdROqe8kCa/wxYXfH9mreOt2VALjew31n/U6q4WcDbg6Zl38b5GAgjHfxvwEZWZA7Tm7Px8Hp2PTouK9uCXzIsdmaO143AtDCn3Hr2BJgT4f2YonckHseOAK3dXcTPiPltlw+6vIZ61FhT4Ln2hVdIhKPEYCc0/Eu7l8D9nJsL5bIDfllwHkOTP0VyMhtuePk9lyjrT9oBlw/z3+W4or3ajXict39c06Lp/ybU3tx5q1hVwM31WBhHiIj5Vbr9WOM6+f5WRdGXArAHxwXcB/H9mKLLFqktOjxwOwqv/pXICW35I6XW9pfj7ocxmZx/Tw7aW8uBcB1QMxROiPZNJGmZW5Hl8zLTyeI8/90H5e/A1yFspfckitEnXdj8+iYMR4wyrFZJ7tSuQwL7loAtqVL9sT9yCLWyPx8h07NLEX1K8CBoKNAtiFYcfm/wHLgXrk5Z979BkFbdE/cR3N2EmzGoQDIb1D1cTuq+BxNJgAAMi+3hmAPgKVR58Vwwucc2/NFxckcEmeNVc7Lv4lrRyB8ybE9w4gC18/xs7JkxVsuDLmOvvtLx/a+7NieYdSV7hD3rp9jZ+3MtQD83LG9XfTbqQE9LdgY2GjiwD1wvwbgUVeGXAuAs4yVMSYEm4ZRL8aGYDOuAtDyBO7jA8ZlF1zD6A9Jx/beEl9/7cqYUwGQ89vXAI84LvB/6AXJAb0wyBiY6PgxWwJfcWz2YVn6gLN9OMLYgusBx/aGITIuhHwaRqio6HhgmGOzTttXGAJwXwg2Dw3BpmGETRhbwzltX+4FYJD+EvdBQjN6Ycq1khpGaGjiq8MJpnW75J/itTzu0qBzAZBzCl3AMsdm3wdkXOfVMMJCkQzBc+uSZVJY7nR30XC24VbCWJZ6TCh5NYxwCON5dd6uwhEApIj70Nfj9YKU65BKhuEcP3HgzoBrx/VaoOg6r6EIgFyQfwV40LHZQcCUMPJrGI6ZgtuVtgAPeJ0rna8ADWkEAMBdIdicpuclw8yzYdSEjh3rASeFYDqM9hSqANwNOHVYALvgic0MNGKLtmgK2MWx1S7gnjDyG5oAyAUdfwNWhmD69LDybBgOOMO9Sbnf61z5YhiZDXc4rdwWgtWv6vmpvUPNt2H0Az8xZm/cT/0FQmlHQNgCAHcSxK9zzTkh59sw+sO5uI39D/A2aCjv/xCyAMiFHf8i8AW4ZrKeb3ECjPjgJ8aMIJwp63d6nSvfDCvf9fCo3xCCzRai2WHXMDbFhbj/6Q/CaT/rCF8ABresBP47BMtH63mpPULPv2H0gZ8Y8wngqBBMPyWr9adh5j10AZBz2xWlLQTTg4BLws6/YVTAJYTT+7fJypWhZrw+k2pUbgScRDHtwWQ9L7VvXcpgGL3gJ8bsB0wOwfQbIDeGnf+6CIB8J/86MD+k/H9fZ4yuRzEMYwN0330Brsa95x9gntd5/xthl6Ge02p/hPsFQgBfZvWWE+tYDsMAQHfc/lDCCV3fRdBeQqduAiDf7niWcH4SBLhGz7W4gUb96EqMHU7Q+4fBIq9zxfP1KEe9F9ZcGZLdjyNiPwsadUOCn/1cx/uHYC+RsNpJb+WoL3pJqgiML22ZUvGx72veQ9lXruxwsmmiYWwKPzF2JPArYPCGD2gJ7eVP3YS1jdLzXuf9dYt+FcXS2otDsrsFMEe/lWiJoExGk6DjxrUAc4DBYZgnvPbRK3UXAPlOx6OEENmkmwNQ74x6l8loHtTTM4ADQjKf9zrvd72/5maJKrjGBbiPFVDiMj0ntVdE5TIGMH5i7F7AZWGZJ/Ar1JVIBEC+0/EEsCgk80OBm/Xc9BZRlM0YmGhi7BDgFoLnKwwWeJ33P1nvckUZXut84N2QbO+Dat08qcbAR5ErgL1DMr+aiBa3RSYAclHH88CPQ7zF6frNtOuNGYwmxE+MyxBuJKprvc77/xRF2aIOsPlfwD9Csi3ATfrN9K4Rl9FoYPzEuF2BGwnvJ/O/g1weVfkiFQC5qON14LwQb7EtcKd+I22zBI2q6Ro/djhBNN5tQ7zNuV7n8tDn/G+KqEcAMLhlPvCzEO8wCphjC4aMatBJk0RE5gD7hHibB2Wof0uU5YxcAOSCdgWmA2tCvM2RvLWVTRU2KkbfeuN84MgQb/EeMF3uXak1W6qByAUAQGZ0PAlcE/JtLtWz04dFXVYj/viJ8ZOBS0O+zfe8zuVPRV3WWAhAgFwMPB3mDYD5enY6jOWbxgDBT4z/MnAT4a6TeUo0tAlFVREbAZCL86uAEwhvhiAEkzju1bPSn4m6vEb88BPj9wbuBYaEeJsu4HhZsjysOTBVERsBAJCLOx4Gvh/ybbYBluhZ6U9EXV4jPvjJ8XsAnQTPR5h8z+tc/vOoy1siVgIAgPJtIOwpkTsBy/XM9G5RF9eInq7E+F1RlhM8F2HyhAgzoi5vObETALm0412CEMurQr7VR4D7TQSam65EYleBFcBHQ77V28BRUlz+XtRlLid2AgAgl3T8DjirDrf6OLBSz0zb/gJNSFcisYfAA4QT2acHcobXufwPUZe5J7EUAAD+8WIb4a0YLOejKD/VM9L/FnWRjfrhJxKfEfgp4ff8ALfJAV+cG3WZe6PuIcGqQb+T3BpffgEEDrtqw4ipVHP960BWrs0/GHW5jXDxE4n/Dyxm3RTfCsJ69T/tKXw+6y25L4x9MWomviMAQC4pvEGw4eLbdbjdNijL9PR0GBs8GjHBTyQmAUsJd35/iTeBQ+Pa+CHmI4ASemHqUJSF6/IbzgigdAwis6z6++Vy3eNRF91whI4ejQ4bfg7o5WzU8YUyAlBgole8796oy745Yj0CKCGXddxJsHS4HnjAdxn6oRv19OywqMtu1I6OTw7RYcPnE4Tbrtczf3HcGz80iAAAMFi/A9xZxzsei/o/1a+nPxZ10Y3+4yeSH1XhQeC4Ot52gQxZ2xAb1zbEK0AJPS89DNEVwGeDhNKJTR379QrQM+0V4Gj5cX5J1OU3qsNPJMcDNwM7rE8N1eEH8IioflU671sddfkroaEEAEDPT30AeBjYo04CAOCjXIXwbflxPsxly4YDNJkcrCqXgJ5Dfd73SzwNfMErLvtn1HVQKQ0nAAB6fmoEykOUpm6GLwCl42Mox8jM/DNR14HRO34i+QmQm4H969Dbl6f9Hfi8V1z2QtR1UA0NKQAAel7qM8BKgp/vuhN7Hp0LACjvAOciXqv8pD3MlYtGFWg2K7qm61QCR9+W3am9XRlG2qvAaK+47LdR10O1NKwAAOh5qS8AS9Duf3h9BKB0/ClworTmn426HpodP5keAToHZfSGZ+oiAG8CY7zistis8KuGhhYAAD0v9RWUPDC8zgIAsBrlu6heKW0dsVrk0QxoOruF+v43gQtAh23cPkMXgLeBhFdc2rCzRxteAAD0W6kDgcUoQfTf+glA6fgMyhnSlg9rz0OjB34yPR64Fvh/QYpSZwF4G8h4xaUroq6LWhgQAgCg56a+ArQDW0UgAKVjAeUcmZ3/fdT1MVDxk9k9wb8aSG14pq4C8CaQ9opLfxp1fdTKgBEAAD039UUgh3ZHdam/AICyFpiPcolcl/9L1HUyUPCTmQ8DFwFTQQdtfEXdBOA1IOkVlz4adZ24YEAJAICek9qbILTTThEJQOm4GpiLcoXMyf816nppVPxkZmfgHOBk1m3MuYnGGb4AvAiM9YpLG87bvykGnAAA6DmpPYACKiOChNKJCo/9+c7mheBGVK+WuR3PRV03jYKfzO4GfAN0KhvtyBuJADyjkGgpLnk+6rpxyYAUAAA9J7UjKjlg/4gFoHTsIliDfi0f2e9BmTEj6iqKHTpjBvrYr75IsBHnwUBLVQ02PAH4GZD1ikteibqOXDNgBQBAv5keDtyEckiQUDrRx7Gaa/t3fBJow9dbZV5HZPvCxQU/cdDWiB4BejIbbcUVuQDcoR5TWzqWhB2jMhIGtAAA6DlZD9+/DPgWWmE8gUquqfUYfF4F3IlyE8gKmZfrirq+6oVmMi3a5Y0GjgUOAbasucG6FQAFLhW8GVIs9nbBgGDAC0AJ/UZ6MsoNwJYxEoDy44vAQpS7QR6U+bkBN81YMxlPfe/zBFGeDkX5cI8revtW5WnuBOAt0CleccldUddZ2DSNAADo2enPEPS4m3cObu5ceAJQ/vkfBHMKCsAKuTHfMKvLeuJnstuAHIiSApIoO25U/k0nVJfmxt7TwCFesbMp5nI0lQAA6Nnp93ePBCbGWADKP/uo/IIgfPUDwM/kptxrUdfjpvAzmW0R7wDgSwRz8/8daOmzrL0nVJdWu72FICd6xeKbkVVgnWk6AQDQGaPhja2+hnIVMDTeAiA90xR4FngU5QngSZSnuDX3Yr3/mf6EzA6IjAT2QdkH2BflkyAb+loqKWvvCdWl9d/eauBM2ep9bbKoHpHo40NTCkAJPTP9GeA2lE8FCeUnQz72lbbus/Q1Qih9fgV4DuU54AXgLyh/Bf6B8hIqr7GKt6S9vU+Hlh6VEFYPep/CNiA7ouwEfJhgD4VdgBEEAVm2770sPSZgVVLW3hOqS+ufvSdBj/KKnb/rq14GIk0tAAB6ZmooKv8FnIGWRY9pPAGo5PxagngG7wCrVaWLYLfaFpQWgtHQcGA4MKgf9htJAHzgGvH9C2XJkljs1BsFTS8AJfSM9JdR5gDBNmEDUwA2SFOVmr7fwALwDHCCVyw+RJPTOFGBQ0auzT+AymeA7xMs6DEGHmuB7ynsbY0/wEYAvaD/md4bmE1/phHbCICYjgAeBU7xioVfY6zDRgC9ID/K/xr4HMrJwMtR58eoiZeBaaL+F6zxb4yNAPpAv57aDpWLgFOAwTYCqOR8LEYAa0BnIlziFQqxnTcRNSYAFaKnpfdAuBLlIEBMAIirAChwN3CeV+ywgK19YAJQJXpa+t+By1G+GiSUTlR57Ctt3WcTgIrTlGXAhV6x4zGMijAB6Cd6avpLwEUo/xEklE5UeOwrbd1nE4AK0paDXuIVOho+Rl+9MQGoET0l/XngPILFLpW/GvSVtu6zCcAm0hTIA1d4hfwjGP3CBMAROj29F3A6ytHAMBOAKr/fe0JvaatAbwV+4BXyT2HUhAmAY3RaagdETkSZBuxqAlDh93tPKE97AZiNyFyvo33AheaKChOAkNCT0x7KeJSpQBZli+BE+UU9jr1+bmoBeA80B8yVFpZKbuAFSYkaE4A6oCemdgA5AjgC5QDYRGiyXj83nQAo8BhwK3C7V2i3iVghYgJQZ/SE9O4EMfAmouxPueMQmlUAFPgV6CJgoVdo/6PDKjc2gwlAhOjx6Y8BCZQM8B+UOw9hoAvAOygrgQ4g5xUW2y5KEWACEBN0SmoIIl9AGQd8iSC6zuABJABrgV91N/plAg9Jx+LVUdS1sR4TgJiiU5Jbod4BwGdR+RxBbL0dG0gAXkJ5nGAV3qMCj0hu8VtR16uxISYADYQem9kZZRQwEtgTZSRBAJOtIxSAN1CeJYim+1uU3wFPyqhRf7bdj+KPCUCDo6NHw85b74jobsCHUT4GfJRgtLATsD3KtsA2BHsiDF733U0LwBrgbZTXCXbD/SfKPwh69b8DfwFeQHleBg95qdkCaQ4k/g9Ufww3y8Cw9AAAAC56VFh0ZGF0ZTpjcmVhdGUAAHjaMzIwtNA1MNE1MgsxsLAyNrMyMNQ2MLAyMAAAQhUFEYVN5YkAAAAuelRYdGRhdGU6bW9kaWZ5AAB42jMyMLTQNTDRNTILMbCwMjazMjDUNjCwMjAAAEIVBRGsck0BAAAAAElFTkSuQmCC"
SYS_PORT=0
SYS_BIND="0.0.0.0"
# DEBUG VALUE - LEAVE BLANK
SYS_CONFIG_FILE_NAME="airport.json"
SYS_CONFIG=None
SYS_COUNTER_200=0
SYS_COUNTER_404=0
SYS_COUNTER_ENDPOINTS=0
SYS_START_TIME=time.time()
SYS_CPU=0
SYS_RAM=0
# DEBUG VALUE - LEAVE BLANK
SYS_LOG_FILE="airport.log"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho

def err(sev,title,reporttolog,exitafter):
    global SYS_LOG_FILE
    TMP_LINE= "[" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "][" + str(sev).upper() + "]: " + str(title)
    print(TMP_LINE)
    if (SYS_LOG_FILE != ""):
        try:
            f = open(SYS_LOG_FILE,'a+')
            f.write(TMP_LINE + "\n")
            f.close()
        except:
            pass
    if (exitafter == 1):
        print("")
        sys.exit(0)

print("")
print(" Airport - API Endpoing Manager")
print(" Released under the MIT license")

for ar in sys.argv:
    if (ar.lower().startswith("--confiig=")):
        SYS_CONFIG_FILE_NAME=ar.replace("--config=","")
    if (ar.lower().startswith("--log=")):
        SYS_LOG_FILE=ar.replace("--log=","")

if (str(SYS_CONFIG_FILE_NAME) == ""):
    err('E', 'Missing configuration file definition. Use --oonfig to set the file name or see documentation.', 0,1)

if (os.path.isfile(SYS_CONFIG_FILE_NAME) == False):
    err('E','Configuration file does not exist or you do not have permissions [' + str(SYS_CONFIG_FILE_NAME) + ']',0,1)

try:
    f = open(SYS_CONFIG_FILE_NAME)
    SYS_CONFIG=json.load(f)
    f.close()
except:
    err('E','Configuration file is malformed/JSON is malformed. Check the configuration file and try again.',0,1)

if (SYS_CONFIG["port"] == ""):
    err('E','Invalid/missing port number in the configuration file.',0,1)

try:
    SYS_PORT=int(SYS_CONFIG["port"])
except:
    err('E','Invalid/missing port number in the configuration file.',0,1)

if (SYS_CONFIG["bind"] == ""):
    err('I','The bind parameter is empty. Using "0.0.0.0" instead.',0,0)
    SYS_BIND="0.0.0.0"

TMP_ENDPOINTS=[]
for u in SYS_CONFIG["endpoints"]:
    if (str(u["path"]) in TMP_ENDPOINTS):
        err('E','Endpoint [' + str(u["path"]) + '] is defined more than once. Please correct and try again.',0,1)
    TMP_ENDPOINTS.append(str(u["path"]))

endpoint_number = 1
for u in SYS_CONFIG["endpoints"]:
    if (str(u["path"]).startswith("/") == False):
        err('E','Endpoing number ' + str(endpoint_number) + ' Is not started with "/" - please start it with this character and try again.',0,1)
    if (str(u["path"]) == "/manager"):
        err('E','The "/manager" URL is a preserved path. You can not use it. Please correct the issue and try again.',0,1)
    if (str(u["type"]) != "cmd"):
        err('E','The type of the action is invalid. Supported actions are just "cmd" at this stage.',0,1)
    if (str(u["command"]) == ""):
        err('E','The command is missing for endpoint number ' + str(endpoint_number) + '. Check configuration and try again.',0,1)
    if (str(u["enabled"]) not in ['1','0']):
        err('E','Invalid enabled value for endpoint number ' + str(endpoint_number) + '. Check configuration and try again.',0,1)
    if (str(u["method"]) == ""):
        err('E', 'Invalid/missing invokation methods value for endpoint number ' + str(endpoint_number) + '. Check configuration and try again.', 0, 1)
    if (str(u["method"]).upper() not in ['GET','POST']):
        err('E', 'Invalid/missing invokation methods value for endpoint number ' + str(endpoint_number) + '. Check configuration and try again.', 0, 1)
    endpoint_number = endpoint_number + 1

def exec_url_command():
    global SYS_COUNTER_404
    global SYS_COUNTER_200
    ht = ''
    tmp_path = ''
    tmp_command = ''
    tmp_is_found=0
    tmp_mime = ""
    tmp_output = ''
    tmp_args = ''
    for u in SYS_CONFIG["endpoints"]:
        if (str(u["path"]) == request.path):
            tmp_is_found = 1
            SYS_COUNTER_200=SYS_COUNTER_200+1
            tmp_path = request.path
            tmp_command = str(u["command"])
            tmp_mime = str(u["mime"])
            tmp_silent = str(u["silent"])
            ht = ht + 'PATH: ' + request.path + ',METHOD: ' + str(request.method) + ',COMMAND: ' + str(u["command"]) + ' '
            if (request.method == 'GET'):
                for ar in request.args:
                    tmp_args = tmp_args + str(ar) + '=' + str(request.args.get(str(ar))) + ','
                    tmp_args = tmp_args.rstrip(",")
            if (request.method == 'POST'):
                for ar in request.form:
                    tmp_args = tmp_args + str(ar) + '=' + str(request.form.get(str(ar))) + ','
                    tmp_args = tmp_args.rstrip(",")
            try:
                on.environ['AIRPORT_ARGS'] = tmp_args
                tmp_output = subprocess.getoutput(tmp_command)
            except:
                tmp_output = ''
            ht = ht + tmp_output
            if (tmp_silent == "1"):
                ht = ''
            r = Response(response=ht, status=200, mimetype=str(tmp_mime))
            return r
    ht = ht + ''
    r = Response(response=ht, status=200, mimetype="text/plain")
    return r

@app.errorhandler(404)
def err404(e):
    global SYS_COUNTER_404
    global SYS_COUNTER_200
    if (str(request.path).lower() != "/favicon.ico"):
        SYS_COUNTER_404=SYS_COUNTER_404+1
    return ''

@app.errorhandler(405)
def err405(e):
    global SYS_COUNTER_404
    global SYS_COUNTER_200
    if (str(request.path).lower() != "/favicon.ico"):
        SYS_COUNTER_404=SYS_COUNTER_404+1
    return ''

@app.errorhandler(500)
def err500(e):
    global SYS_COUNTER_404
    global SYS_COUNTER_200
    SYS_COUNTER_404=SYS_COUNTER_404+1
    return ''

for u in SYS_CONFIG["endpoints"]:
    SYS_COUNTER_ENDPOINTS=SYS_COUNTER_ENDPOINTS+1
    app.add_url_rule(str(u["path"]),str(u["name"]),exec_url_command, methods=str(u["method"]).split(","))

if (str(SYS_CONFIG["adminenabled"]) == "1"):
    SYS_COUNTER_ENDPOINTS=SYS_COUNTER_ENDPOINTS+1
    err('I','Adding the /manager URL as the "adminenabled" is set to 1.',0,0)
    @app.route('/manager', methods=['GET'])
    def index():
        global SYS_CPU
        global SYS_RAM
        ht = ''
        ht = ht + '<!DOCTYPE html>'
        ht = ht + '<html>'
        ht = ht + '<head>'
        ht = ht + '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
        ht = ht + '<title>Airport Status</title>'
        ht = ht + '<style> html * { font-family: Monospace; user-select: none; } </style>'
        ht = ht + '</head>'
        ht = ht + '<body>'
        ht = ht + '<img src="' + SYS_IMG + '" style="position: absolute; top: 10px; left: 10%; width: 48px; height: 48px; border: none;"/>'
        ht = ht + '<label style="position: absolute; top: 11px; left: calc(10% + 60px); font-size: 20px; font-weight: normal; color: red;">Airport</label>'
        ht = ht + '<label style="position: absolute; top: 36px; left: calc(10% + 60px); font-size: 14px; font-weight: lighter; color: gray;">API Endpoint Manager</label>'
        ht = ht + '<table cellspacing="0" cellpadding="0" border="0" style="position: absolute; top: 70px; left: 10%; right: 10%; width: 80%; height: auto; border: none; font-size: 12px;">'
        ht = ht + '<tr style="height: 32px;">'
        ht = ht + '<td style="width: 16%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Valid Calls Count</td>'
        ht = ht + '<td style="width: 16%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Invalid Calls Count</td>'
        ht = ht + '<td style="width: 17%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Active Endpoints</td>'
        ht = ht + '<td style="width: 17%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Uptime (Min.)</td>'
        ht = ht + '<td style="width: 17%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">CPU (%)</td>'
        ht = ht + '<td style="width: 17%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">RAM (%)</td>'
        ht = ht + '</tr>'
        ht = ht + '<tr style="height: 68px;">'
        ht = ht + '<td style="width: 16%; padding-left: 4px; color: black; font-size: 40px; font-weight: bold;">' + str(SYS_COUNTER_200) + '</td>'
        ht = ht + '<td style="width: 16%; padding-left: 4px; color: black; font-size: 40px; font-weight: bold;">' + str(SYS_COUNTER_404) + '</td>'
        ht = ht + '<td style="width: 17%; padding-left: 4px; color: black; font-size: 40px; font-weight: bold;">' + str(SYS_COUNTER_ENDPOINTS) + '</td>'
        tmp_sec = 0
        if (int(time.time() - SYS_START_TIME) < 60):
            tmp_sec = 1
        else:
            tmp_sec = int(int(time.time() - SYS_START_TIME) / 60)
        ht = ht + '<td style="width: 17%; padding-left: 4px; color: black; font-size: 40px; font-weight: bold;">' + str(tmp_sec) + '</td>'
        ht = ht + '<td style="width: 17%; padding-left: 4px; color: black; font-size: 40px; font-weight: bold;">' + str(SYS_CPU) + ' %</td>'
        ht = ht + '<td style="width: 17%; padding-left: 4px; color: black; font-size: 40px; font-weight: bold;">' + str(SYS_RAM) + ' %</td>'
        ht = ht + '</tr>'
        ht = ht + '</table>'
        ht = ht + '<table cellspacing="0" cellpadding="0" border="0" style="position: absolute; top: 190px; left: 10%; right: 10%; width: 80%; height: auto; border: none; font-size: 12px;">'
        ht = ht + '<tr style="height: 32px;">'
        ht = ht + '<td style="width: 20%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Path/URL</td>'
        ht = ht + '<td style="width: 60%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Name/Description</td>'
        ht = ht + '<td style="width: 10%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Methods</td>'
        ht = ht + '<td style="width: 10%; padding-left: 4px; border-bottom: 1px dotted gray; color: gray;">Enabled</td>'
        ht = ht + '</tr>'
        ht = ht + ''
        ht = ht + '<tr style="height: 32px;">'
        ht = ht + '<td style="width: 20%; padding-left: 4px; color: black;">/manager</td>'
        ht = ht + '<td style="width: 60%; padding-left: 4px; color: black;">Internal system status web page</td>'
        ht = ht + '<td style="width: 10%; padding-left: 4px; color: black;">GET</td>'
        ht = ht + '<td style="width: 10%; padding-left: 4px; color: black;">Yes</td>'
        ht = ht + '</tr>'
        for u in SYS_CONFIG["endpoints"]:
            ht = ht + '<tr style="height: 32px;">'
            ht = ht + '<td style="width: 20%; padding-left: 4px; color: black;">' + str(u["path"]) + '</td>'
            ht = ht + '<td style="width: 60%; padding-left: 4px; color: black;">' + str(u["name"]) + '</td>'
            ht = ht + '<td style="width: 10%; padding-left: 4px; color: black;">' + str(u["method"]) + '</td>'
            if (str(u["enabled"]) == "1"):
                ht = ht + '<td style="width: 10%; padding-left: 4px; color: black;">Yes</td>'
            else:
                ht = ht + '<td style="width: 10%; padding-left: 4px; color: black;">No</td>'
            ht = ht + '</tr>'
        ht = ht + '</table>'
        ht = ht + '</body>'
        ht = ht + '</html>'
        r = Response(response=ht, status=200, mimetype="text/html")
        return r

def collect_system_metrics():
    global SYS_CPU
    global SYS_RAM
    SYS_CPU=int(psutil.cpu_percent(2))
    SYS_RAM = int(psutil.virtual_memory().percent)

def system_metrics():
    schedule.every(20).seconds.do(collect_system_metrics)
    while True:
        schedule.run_pending()
        time.sleep(1)

log = logging.getLogger('werkzeug')
log.disabled = True
log.setLevel(logging.ERROR)
SYS_CPU=int(psutil.cpu_percent(2))
SYS_RAM=int(psutil.virtual_memory().percent)
err('I','Binding address = ' + str(SYS_BIND),0,0)
err('I','Binding port = ' + str(SYS_PORT),0,0)
t = threading.Thread(target=system_metrics)
t.start()
app.run(debug=False, host=str(SYS_BIND), port=int(SYS_PORT))
