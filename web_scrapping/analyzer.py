from bs4 import BeautifulSoup

html_content = """
<table class="default_table welfare_select_table">
  <caption>복리후생 리스트</caption>
  <colgroup>
    <col style="width:20%">
    <col style="width:20%">
    <col style="width:20%">
    <col style="width:20%">
    <col style="width:20%">
  </colgroup>
  <tbody>
    <tr>
      <th>지원금/보험</th>
      <th>급여제도</th>
      <th>선물</th>
      <th>교육/생활</th>
      <th>근무 환경</th>
    </tr>
    <tr>
      <td>
        <ul class="chk_list">
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp407" name="welfare_cd[]" value="corp407" data-description="건강검진" data-pass-onload-refresh="y" data-gtm-form-interact-field-id="0">
              <label class="lbl" for="welfare_cd_corp407">건강검진</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp408" name="welfare_cd[]" value="corp408" data-description="의료비지원(본인)" data-pass-onload-refresh="y" data-gtm-form-interact-field-id="1">
              <label class="lbl" for="welfare_cd_corp408">의료비지원(본인)</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp409" name="welfare_cd[]" value="corp409" data-description="금연수당" data-pass-onload-refresh="y" data-gtm-form-interact-field-id="2">
              <label class="lbl" for="welfare_cd_corp409">금연수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp411" name="welfare_cd[]" value="corp411" data-description="직원대출제도" data-pass-onload-refresh="y" data-gtm-form-interact-field-id="3">
              <label class="lbl" for="welfare_cd_corp411">직원대출제도</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp417" name="welfare_cd[]" value="corp417" data-description="각종 경조사 지원" data-pass-onload-refresh="y" data-gtm-form-interact-field-id="4">
              <label class="lbl" for="welfare_cd_corp417">각종 경조사 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp419" name="welfare_cd[]" value="corp419" data-description="단체 상해보험" data-pass-onload-refresh="y" data-gtm-form-interact-field-id="5">
              <label class="lbl" for="welfare_cd_corp419">단체 상해보험</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp439" name="welfare_cd[]" value="corp439" data-description="의료비지원(가족)" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp439">의료비지원(가족)</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp440" name="welfare_cd[]" value="corp440" data-description="체력단련실운영" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp440">체력단련실운영</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp441" name="welfare_cd[]" value="corp441" data-description="헬스비 지급" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp441">헬스비 지급</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp442" name="welfare_cd[]" value="corp442" data-description="무료진료지정병원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp442">무료진료지정병원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp486" name="welfare_cd[]" value="corp486" data-description="본인학자금" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp486">본인학자금</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp487" name="welfare_cd[]" value="corp487" data-description="업무활동비 지급" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp487">업무활동비 지급</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp488" name="welfare_cd[]" value="corp488" data-description="문화생활비" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp488">문화생활비</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp489" name="welfare_cd[]" value="corp489" data-description="통신비 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp489">통신비 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp490" name="welfare_cd[]" value="corp490" data-description="결혼준비 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp490">결혼준비 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp491" name="welfare_cd[]" value="corp491" data-description="해외여행 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp491">해외여행 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp492" name="welfare_cd[]" value="corp492" data-description="선택적복리후생" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp492">선택적복리후생</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp495" name="welfare_cd[]" value="corp495" data-description="복지카드/포인트" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp495">복지카드/포인트</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp496" name="welfare_cd[]" value="corp496" data-description="난임 치료 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp496">난임 치료 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp497" name="welfare_cd[]" value="corp497" data-description="주요 제품 직원 할인" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp497">주요 제품 직원 할인</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp498" name="welfare_cd[]" value="corp498" data-description="자녀학자금" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp498">자녀학자금</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp534" name="welfare_cd[]" value="corp534" data-description="사내 결혼식장 제공" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp534">사내 결혼식장 제공</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp537" name="welfare_cd[]" value="corp537" data-description="내일채움공제" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp537">내일채움공제</label>
            </span>
          </li>
        </ul>
      </td>
      <td>
        <ul class="chk_list">
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp400" name="welfare_cd[]" value="corp400" data-description="퇴직연금" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp400">퇴직연금</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp401" name="welfare_cd[]" value="corp401" data-description="인센티브제" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp401">인센티브제</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp402" name="welfare_cd[]" value="corp402" data-description="상여금" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp402">상여금</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp403" name="welfare_cd[]" value="corp403" data-description="장기근속자 포상" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp403">장기근속자 포상</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp404" name="welfare_cd[]" value="corp404" data-description="우수사원포상" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp404">우수사원포상</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp405" name="welfare_cd[]" value="corp405" data-description="스톡옵션" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp405">스톡옵션</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp406" name="welfare_cd[]" value="corp406" data-description="퇴직금" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp406">퇴직금</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp420" name="welfare_cd[]" value="corp420" data-description="성과급" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp420">성과급</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp421" name="welfare_cd[]" value="corp421" data-description="야근수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp421">야근수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp422" name="welfare_cd[]" value="corp422" data-description="휴일(특근)수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp422">휴일(특근)수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp423" name="welfare_cd[]" value="corp423" data-description="연차수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp423">연차수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp424" name="welfare_cd[]" value="corp424" data-description="직책수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp424">직책수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp425" name="welfare_cd[]" value="corp425" data-description="자격증수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp425">자격증수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp426" name="welfare_cd[]" value="corp426" data-description="장기근속수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp426">장기근속수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp427" name="welfare_cd[]" value="corp427" data-description="위험수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp427">위험수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp428" name="welfare_cd[]" value="corp428" data-description="가족수당" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp428">가족수당</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp499" name="welfare_cd[]" value="corp499" data-description="4대 보험" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp499">4대 보험</label>
            </span>
          </li>
        </ul>
      </td>
      <td>
        <ul class="chk_list">
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp434" name="welfare_cd[]" value="corp434" data-description="명절선물/귀향비" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp434">명절선물/귀향비</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp435" name="welfare_cd[]" value="corp435" data-description="창립일선물지급" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp435">창립일선물지급</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp436" name="welfare_cd[]" value="corp436" data-description="생일선물/파티" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp436">생일선물/파티</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp437" name="welfare_cd[]" value="corp437" data-description="크리스마스 선물" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp437">크리스마스 선물</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp438" name="welfare_cd[]" value="corp438" data-description="결혼기념일선물" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp438">결혼기념일선물</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp500" name="welfare_cd[]" value="corp500" data-description="도서 무제한 제공" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp500">도서 무제한 제공</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp501" name="welfare_cd[]" value="corp501" data-description="임신/출산 선물" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp501">임신/출산 선물</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp502" name="welfare_cd[]" value="corp502" data-description="웰컴키트 지급" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp502">웰컴키트 지급</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp503" name="welfare_cd[]" value="corp503" data-description="생일자 조기퇴근" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp503">생일자 조기퇴근</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp532" name="welfare_cd[]" value="corp532" data-description="장기근속 선물" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp532">장기근속 선물</label>
            </span>
          </li>
        </ul>
      </td>
      <td>
        <ul class="chk_list">
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp100" name="welfare_cd[]" value="corp100" data-description="창립일행사" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp100">창립일행사</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp101" name="welfare_cd[]" value="corp101" data-description="우수사원시상식" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp101">우수사원시상식</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp102" name="welfare_cd[]" value="corp102" data-description="워크샵" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp102">워크샵</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp103" name="welfare_cd[]" value="corp103" data-description="플레이샵" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp103">플레이샵</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp200" name="welfare_cd[]" value="corp200" data-description="신규 입사자 교육(OJT)" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp200">신규 입사자 교육(OJT)</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp201" name="welfare_cd[]" value="corp201" data-description="직무능력향상교육" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp201">직무능력향상교육</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp202" name="welfare_cd[]" value="corp202" data-description="리더십 강화교육" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp202">리더십 강화교육</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp203" name="welfare_cd[]" value="corp203" data-description="해외연수지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp203">해외연수지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp204" name="welfare_cd[]" value="corp204" data-description="도서구입비지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp204">도서구입비지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp205" name="welfare_cd[]" value="corp205" data-description="MBA과정지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp205">MBA과정지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp206" name="welfare_cd[]" value="corp206" data-description="멘토링제도" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp206">멘토링제도</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp207" name="welfare_cd[]" value="corp207" data-description="외국어 교육 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp207">외국어 교육 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp208" name="welfare_cd[]" value="corp208" data-description="사이버연수원운영" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp208">사이버연수원운영</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp209" name="welfare_cd[]" value="corp209" data-description="자격증취득지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp209">자격증취득지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp210" name="welfare_cd[]" value="corp210" data-description="교육비 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp210">교육비 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp211" name="welfare_cd[]" value="corp211" data-description="자기계발비 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp211">자기계발비 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp413" name="welfare_cd[]" value="corp413" data-description="구내식당(사원식당)" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp413">구내식당(사원식당)</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp415" name="welfare_cd[]" value="corp415" data-description="점심식사 제공" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp415">점심식사 제공</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp416" name="welfare_cd[]" value="corp416" data-description="저녁식사 제공" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp416">저녁식사 제공</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp418" name="welfare_cd[]" value="corp418" data-description="사내동호회 운영" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp418">사내동호회 운영</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp429" name="welfare_cd[]" value="corp429" data-description="사우회(경조사회)" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp429">사우회(경조사회)</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp469" name="welfare_cd[]" value="corp469" data-description="아침식사 제공" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp469">아침식사 제공</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp470" name="welfare_cd[]" value="corp470" data-description="간식 제공" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp470">간식 제공</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp471" name="welfare_cd[]" value="corp471" data-description="식비 지원" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp471">식비 지원</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp472" name="welfare_cd[]" value="corp472" data-description="음료제공(차, 커피)" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp472">음료제공(차, 커피)</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp493" name="welfare_cd[]" value="corp493" data-description="해외주재원 제도" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp493">해외주재원 제도</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp494" name="welfare_cd[]" value="corp494" data-description="우리사주제도" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp494">우리사주제도</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp504" name="welfare_cd[]" value="corp504" data-description="해외 워크샵" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp504">해외 워크샵</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp505" name="welfare_cd[]" value="corp505" data-description="점심시간 연장제도" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp505">점심시간 연장제도</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp506" name="welfare_cd[]" value="corp506" data-description="취미 프로그램 운영" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp506">취미 프로그램 운영</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp507" name="welfare_cd[]" value="corp507" data-description="가족 초청 행사" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp507">가족 초청 행사</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp531" name="welfare_cd[]" value="corp531" data-description="신규입사자 멘토 제도" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp531">신규입사자 멘토 제도</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp536" name="welfare_cd[]" value="corp536" data-description="컨퍼런스 개최" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp536">컨퍼런스 개최</label>
            </span>
          </li>
        </ul>
      </td>
      <td>
        <ul class="chk_list">
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp443" name="welfare_cd[]" value="corp443" data-description="수유실" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp443">수유실</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp444" name="welfare_cd[]" value="corp444" data-description="사내 어린이집 운영" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp444">사내 어린이집 운영</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp449" name="welfare_cd[]" value="corp449" data-description="휴게실" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp449">휴게실</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp450" name="welfare_cd[]" value="corp450" data-description="수면실" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp450">수면실</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp451" name="welfare_cd[]" value="corp451" data-description="회의실" data-pass-onload-refresh="y">
              <label class="lbl" for="welfare_cd_corp451">회의실</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">
              <input type="checkbox" id="welfare_cd_corp452" name="welfare_cd[]" value="corp452" data-description="공기청정기" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp452">공기청정기</label>
            </span>
          </li>
          <li class="chk_item">
            <span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp453" name="welfare_cd[]" value="corp453" data-description="카페테리아" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp453">카페테리아</label>undefined</span>
          </li>
          <li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp454" name="welfare_cd[]" value="corp454" data-description="게임기" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp454">게임기</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp455" name="welfare_cd[]" value="corp455" data-description="전용 사옥" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp455">전용 사옥</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp457" name="welfare_cd[]" value="corp457" data-description="사내 정원" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp457">사내 정원</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp458" name="welfare_cd[]" value="corp458" data-description="건물 내 경사로" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp458">건물 내 경사로</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp459" name="welfare_cd[]" value="corp459" data-description="휠체어용 난간" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp459">휠체어용 난간</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp460" name="welfare_cd[]" value="corp460" data-description="유도점자블록" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp460">유도점자블록</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp461" name="welfare_cd[]" value="corp461" data-description="장애인 화장실" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp461">장애인 화장실</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp462" name="welfare_cd[]" value="corp462" data-description="장애인 전용주차장" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp462">장애인 전용주차장</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp463" name="welfare_cd[]" value="corp463" data-description="장애인 엘리베이터" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp463">장애인 엘리베이터</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp464" name="welfare_cd[]" value="corp464" data-description="비상경보장치" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp464">비상경보장치</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp465" name="welfare_cd[]" value="corp465" data-description="문턱 없음" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp465">문턱 없음</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp468" name="welfare_cd[]" value="corp468" data-description="유니폼지급" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp468">유니폼지급</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp481" name="welfare_cd[]" value="corp481" data-description="스마트기기" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp481">스마트기기</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp482" name="welfare_cd[]" value="corp482" data-description="노트북" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp482">노트북</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp483" name="welfare_cd[]" value="corp483" data-description="사원증" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp483">사원증</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp484" name="welfare_cd[]" value="corp484" data-description="자회사 제품할인" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp484">자회사 제품할인</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp485" name="welfare_cd[]" value="corp485" data-description="콘도/리조트 이용권" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp485">콘도/리조트 이용권</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp508" name="welfare_cd[]" value="corp508" data-description="사내도서관" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp508">사내도서관</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp509" name="welfare_cd[]" value="corp509" data-description="사무용품 지급" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp509">사무용품 지급</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp510" name="welfare_cd[]" value="corp510" data-description="최고 성능 컴퓨터" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp510">최고 성능 컴퓨터</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp511" name="welfare_cd[]" value="corp511" data-description="안마실/안마의자" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp511">안마실/안마의자</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp512" name="welfare_cd[]" value="corp512" data-description="사내 의원/약국" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp512">사내 의원/약국</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp513" name="welfare_cd[]" value="corp513" data-description="스탠딩 책상" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp513">스탠딩 책상</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp538" name="welfare_cd[]" value="corp538" data-description="비자 발급 지원" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp538">비자 발급 지원</label>undefined</span>undefined</li>undefined
        </ul>undefined
      </td>undefined
    </tr>undefined<tr>undefined<th>조직문화</th>undefined<th>출퇴근</th>undefined<th>리프레시</th>undefined</tr>undefined<tr>undefined<td>undefined<ul class="chk_list">undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp309" name="welfare_cd[]" value="corp309" data-description="무제한 연차" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp309">무제한 연차</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp430" name="welfare_cd[]" value="corp430" data-description="노조/노사협의회" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp430">노조/노사협의회</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp431" name="welfare_cd[]" value="corp431" data-description="수평적 조직문화" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp431">수평적 조직문화</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp432" name="welfare_cd[]" value="corp432" data-description="회식강요 안함" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp432">회식강요 안함</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp433" name="welfare_cd[]" value="corp433" data-description="야근강요 안함" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp433">야근강요 안함</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp466" name="welfare_cd[]" value="corp466" data-description="자유복장" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp466">자유복장</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp467" name="welfare_cd[]" value="corp467" data-description="캐주얼데이" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp467">캐주얼데이</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp514" name="welfare_cd[]" value="corp514" data-description="자유로운 연차사용" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp514">자유로운 연차사용</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp515" name="welfare_cd[]" value="corp515" data-description="님/닉네임 문화" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp515">님/닉네임 문화</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp516" name="welfare_cd[]" value="corp516" data-description="출산 장려" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp516">출산 장려</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp518" name="welfare_cd[]" value="corp518" data-description="칼퇴근 보장" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp518">칼퇴근 보장</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp519" name="welfare_cd[]" value="corp519" data-description="반려동물 동반출근" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp519">반려동물 동반출근</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp520" name="welfare_cd[]" value="corp520" data-description="문화 회식" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp520">문화 회식</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp533" name="welfare_cd[]" value="corp533" data-description="사내연애 장려" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp533">사내연애 장려</label>undefined</span>undefined</li>undefined</ul>undefined</td>undefined<td>undefined<ul class="chk_list">undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp410" name="welfare_cd[]" value="corp410" data-description="기숙사 운영" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp410">기숙사 운영</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp412" name="welfare_cd[]" value="corp412" data-description="차량유류비지급" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp412">차량유류비지급</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp414" name="welfare_cd[]" value="corp414" data-description="통근버스 운행" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp414">통근버스 운행</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp473" name="welfare_cd[]" value="corp473" data-description="사택제공" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp473">사택제공</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp474" name="welfare_cd[]" value="corp474" data-description="사원아파트 임대" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp474">사원아파트 임대</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp475" name="welfare_cd[]" value="corp475" data-description="주택자금 융자" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp475">주택자금 융자</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp476" name="welfare_cd[]" value="corp476" data-description="야간교통비지급" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp476">야간교통비지급</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp477" name="welfare_cd[]" value="corp477" data-description="주차장제공" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp477">주차장제공</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp478" name="welfare_cd[]" value="corp478" data-description="주차비지원" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp478">주차비지원</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp479" name="welfare_cd[]" value="corp479" data-description="회사차량 있음" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp479">회사차량 있음</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp480" name="welfare_cd[]" value="corp480" data-description="탄력근무제" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp480">탄력근무제</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp521" name="welfare_cd[]" value="corp521" data-description="주거비 지원" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp521">주거비 지원</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp522" name="welfare_cd[]" value="corp522" data-description="전세자금 대출" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp522">전세자금 대출</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp523" name="welfare_cd[]" value="corp523" data-description="출퇴근 교통비 지원" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp523">출퇴근 교통비 지원</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp524" name="welfare_cd[]" value="corp524" data-description="재택근무" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp524">재택근무</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp525" name="welfare_cd[]" value="corp525" data-description="주 52시간제 준수" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp525">주 52시간제 준수</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp526" name="welfare_cd[]" value="corp526" data-description="주 40시간제 시행" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp526">주 40시간제 시행</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp527" name="welfare_cd[]" value="corp527" data-description="주4.5일" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp527">주4.5일</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp528" name="welfare_cd[]" value="corp528" data-description="주4일" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp528">주4일</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp535" name="welfare_cd[]" value="corp535" data-description="자율 근무제" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp535">자율 근무제</label>undefined</span>undefined</li>undefined</ul>undefined</td>undefined<td>undefined<ul class="chk_list">undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp300" name="welfare_cd[]" value="corp300" data-description="연차" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp300">연차</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp301" name="welfare_cd[]" value="corp301" data-description="여름휴가" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp301">여름휴가</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp302" name="welfare_cd[]" value="corp302" data-description="경조휴가제" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp302">경조휴가제</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp303" name="welfare_cd[]" value="corp303" data-description="반차" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp303">반차</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp304" name="welfare_cd[]" value="corp304" data-description="Refresh휴가" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp304">Refresh휴가</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp305" name="welfare_cd[]" value="corp305" data-description="창립일휴무" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp305">창립일휴무</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp306" name="welfare_cd[]" value="corp306" data-description="근로자의 날 휴무" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp306">근로자의 날 휴무</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp307" name="welfare_cd[]" value="corp307" data-description="휴가비지원" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp307">휴가비지원</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp308" name="welfare_cd[]" value="corp308" data-description="포상휴가" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp308">포상휴가</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp445" name="welfare_cd[]" value="corp445" data-description="산전 후 휴가" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp445">산전 후 휴가</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp446" name="welfare_cd[]" value="corp446" data-description="육아휴직" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp446">육아휴직</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp447" name="welfare_cd[]" value="corp447" data-description="남성출산휴가" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp447">남성출산휴가</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp448" name="welfare_cd[]" value="corp448" data-description="보건휴가" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp448">보건휴가</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp456" name="welfare_cd[]" value="corp456" data-description="휴양시설 제공" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp456">휴양시설 제공</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp529" name="welfare_cd[]" value="corp529" data-description="패밀리데이" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp529">패밀리데이</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp530" name="welfare_cd[]" value="corp530" data-description="시간제 연차" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp530">시간제 연차</label>undefined</span>undefined</li>undefined<li class="chk_item">undefined<span class="inpChk small">undefined<input type="checkbox" id="welfare_cd_corp310" name="welfare_cd[]" value="corp310" data-description="공휴일 휴무" data-pass-onload-refresh="y">undefined<label class="lbl" for="welfare_cd_corp310">공휴일 휴무</label>undefined</span>undefined</li>undefined</ul>undefined</td>undefined</tr>undefined
  </tbody>undefined
</table>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

# 결과를 저장할 딕셔너리
welfare_dict = {}

# 모든 체크박스 input 요소를 찾습니다
checkboxes = soup.find_all('input', type='checkbox', attrs={'name': 'welfare_cd[]'})

# 각 체크박스에서 정보를 추출합니다
for checkbox in checkboxes:
    description = checkbox.get('data-description')
    value = checkbox.get('id').split('_')[-1]
    welfare_dict[description] = value

# 결과 출력
with open("./web_scrapping/welfare_map.txt", "w+") as f:
    for key, value in welfare_dict.items():
            print(f"{key} (welfare_cd={value})", file=f)