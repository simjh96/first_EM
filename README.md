# first_EM

discrete prob & finite sample space ==> categorical distribution으로 표현 가능
모든 sample space 결과는 서로간의 상호작용의 결과로 나타낼 수 있음(수렴 균형 & 1대1 대응)
미분이 어려운 경우 EM으로 쉽게 optimize 가능(첫 rep 에 가장 크게 변함)

missing, latent data & parameter를 observed data로 likelihood maximization
complete EM 에 conditional mean theha_t(상수, 미분하면 0) 를 대신 넣고 MLE
observed likelihood 곡선에 한점에 접하면서 jensen's inequality 로 매번 해당 곡선의 max를 찾아감

해당 categorical case 경우 obs likelihood 는 당연히 partial info 에서 얻을 수 없는 parameter는 full info data로만 계산하듯
EM 방법 역시 그와 정확히 논리가 같음으로 결과도 당연히 iteration에 의해 그러한 정보들은 더이상 update 안됨
[ex) (y1, y2) case 에서 y1|y2 같은 정보는 partial 로 update 안됨]
