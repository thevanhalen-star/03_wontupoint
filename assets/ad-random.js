/* 광고 이미지 1~4번: /ad_image/00N/ 폴더의 이미지 중 하나를 로딩 시 랜덤 선택.
   폴더에 이미지를 추가/삭제하면 아래 개수만 맞춰 주세요 (파일명은 001.jpg, 002.jpg … 연번). */
(function () {
  var COUNT = { 1: 11, 2: 7, 3: 7, 4: 3 };
  var imgs = document.querySelectorAll("img[data-ad]");
  for (var i = 0; i < imgs.length; i++) {
    var n = imgs[i].getAttribute("data-ad");
    var max = COUNT[n];
    if (!max) continue;
    var pick = String(1 + Math.floor(Math.random() * max));
    while (pick.length < 3) pick = "0" + pick;
    imgs[i].src = "/ad_image/00" + n + "/" + pick + ".jpg";
  }
})();
