/**
 * テスト返却スクリプト（Google Classroom + Drive）テンプレート
 *
 * 実行順（この順序を守ること）:
 *   1. createAssignment()  … Classroomに課題を「下書き」で作成（実行後、ログのcourseWorkIdをCONFIGに記入）
 *   2. 成績PDFをDriveフォルダにアップロード → 【アップロード完了を目視確認】
 *   3. shareFiles()        … 各学生本人にのみ閲覧共有
 *                            ※ログの共有件数が名簿人数と一致することを必ず確認
 *   4. notifyFileLinks()   … 【必須】各学生に本人PDFの直リンクをメール送信
 *   5. postGrades()        … 点数を課題に反映（返却状態にして学生に見せる）
 *
 * ─────────────────────────────────────────────────────────
 * 【重要な教訓・厳守】この注意書きを消さないこと
 *   - 課題説明文にDriveフォルダのリンクを載せない。
 *     フォルダ自体は未共有なので学生は誰も開けず、「アクセス権リクエスト」が殺到する
 *     （実際に中間・期末の両方で発生した）。
 *   - フォルダへのアクセス権リクエストは絶対に承認しない
 *     （承認するとその学生が全員分の成績PDFを閲覧できてしまう）。放置してよい。
 *   - DriveApp.addViewer() は共有通知メールを送らない仕様。学生への導線は
 *     (a) notifyFileLinks() の直リンクメール、(b) Driveの「共有アイテム」の2つだけ。
 *   - 教員が手動作成した課題にはAPIから点数を入れられない（@ProjectPermissionDenied）。
 *     課題は必ず createAssignment() で作成したものを使う。
 *   - 返却済み提出物への return 再実行は Precondition failed になるが無害（点数patchは成功する）。
 * ─────────────────────────────────────────────────────────
 *
 * 事前準備:
 *   - script.google.com で新規プロジェクトを作り、このファイルを貼り付ける
 *   - 「サービス +」から Google Classroom API（識別子: Classroom）を追加する
 *   - CONFIG を埋める
 *   - STUDENTS を [学籍番号, メールアドレス, 点数] の配列で埋める（帳票から生成する）
 */

const CONFIG = {
  COURSE_ID: "",        // ClassroomのコースID
  FOLDER_ID: "",        // 成績PDFを入れたDriveフォルダのID
  FORM_URL: "",         // 疑義申告フォームのURL
  COURSE_WORK_ID: "",   // createAssignment() 実行後にログに出るIDを貼る
  TITLE: "テスト結果（AI採点・速報）",
  MAX_POINTS: 100,
  DUE_TEXT: "疑義申告の締切: ○月○日（○）12:00",
  RETURN_TO_STUDENTS: true,
};

// [学籍番号, メールアドレス, 点数]
const STUDENTS = [
  // ["B990001", "example@example.ac.jp", 87],
];

/** 1. 課題を下書きで作成する（説明文にフォルダリンクを載せない） */
function createAssignment() {
  const desc =
    "テストの採点結果（速報）です。\n\n" +
    "【成績票の開き方】\n" +
    "・自分宛にメールで届いた直リンクを開く\n" +
    "・または Google ドライブの「共有アイテム（Shared with me）」から自分の学籍番号のファイルを開く\n" +
    "  （フォルダは共有していません。フォルダを探さないでください）\n\n" +
    "【重要】この採点はAIによる速報です。AIは手書きの読み間違いをすることがあります。\n" +
    "必ず自分の答案画像と照合し、疑義があれば下記フォームから申告してください。\n" +
    CONFIG.FORM_URL + "\n" + CONFIG.DUE_TEXT;

  const cw = Classroom.Courses.CourseWork.create({
    title: CONFIG.TITLE,
    description: desc,
    workType: "ASSIGNMENT",
    state: "DRAFT",
    maxPoints: CONFIG.MAX_POINTS,
  }, CONFIG.COURSE_ID);
  Logger.log("courseWorkId = " + cw.id + " （CONFIG.COURSE_WORK_ID に貼ること）");
}

/** 2〜3. 各PDFを本人のみに閲覧共有する（ファイル名は「学籍番号_氏名.pdf」を想定） */
function shareFiles() {
  const folder = DriveApp.getFolderById(CONFIG.FOLDER_ID);
  const byId = {};
  const files = folder.getFiles();
  while (files.hasNext()) {
    const f = files.next();
    const m = f.getName().match(/(B?\d{6})/);
    if (m) byId[m[1].replace(/^B/, "")] = f;
  }
  let ok = 0, miss = [];
  STUDENTS.forEach(function (s) {
    const f = byId[String(s[0]).replace(/^B/, "")];
    if (!f) { miss.push(s[0]); return; }
    try { f.addViewer(s[1]); ok++; } catch (e) { miss.push(s[0] + ":" + e); }
  });
  Logger.log("共有 " + ok + " 件 / 名簿 " + STUDENTS.length + " 件");
  if (miss.length) Logger.log("未共有: " + miss.join(", "));
  if (ok !== STUDENTS.length) {
    Logger.log("!! 件数が一致しません。PDFのアップロード完了を確認してから再実行してください。");
  }
}

/** 4. 各学生に本人PDFの直リンクをメールする（必須。共有通知は自動では飛ばない） */
function notifyFileLinks() {
  const folder = DriveApp.getFolderById(CONFIG.FOLDER_ID);
  const byId = {};
  const files = folder.getFiles();
  while (files.hasNext()) {
    const f = files.next();
    const m = f.getName().match(/(B?\d{6})/);
    if (m) byId[m[1].replace(/^B/, "")] = f;
  }
  let sent = 0;
  STUDENTS.forEach(function (s) {
    const f = byId[String(s[0]).replace(/^B/, "")];
    if (!f) return;
    MailApp.sendEmail({
      to: s[1],
      subject: "[" + CONFIG.TITLE + "] 採点結果（" + s[0] + "）",
      body:
        s[0] + " さん\n\n採点結果（速報）です。以下のリンクから確認してください。\n" +
        f.getUrl() + "\n\n" +
        "（リンクが開けない場合は Google ドライブの「共有アイテム」からも開けます）\n\n" +
        "この採点はAIによる速報です。AIは手書きの読み間違いをすることがあります。\n" +
        "必ず自分の答案画像と照合し、疑義があれば申告してください。\n" +
        CONFIG.FORM_URL + "\n" + CONFIG.DUE_TEXT + "\n",
    });
    sent++;
  });
  Logger.log("メール送信 " + sent + " 件（Workspaceの上限は1500通/日）");
}

/** 5. 点数を反映して返却する */
function postGrades() {
  const cwId = CONFIG.COURSE_WORK_ID;
  if (!cwId) throw new Error("CONFIG.COURSE_WORK_ID が未設定です");
  const subs = Classroom.Courses.CourseWork.StudentSubmissions.list(
    CONFIG.COURSE_ID, cwId).studentSubmissions || [];
  const emailById = {};
  subs.forEach(function (sub) {
    const prof = Classroom.UserProfiles.get(sub.userId);
    emailById[prof.emailAddress.toLowerCase()] = sub;
  });
  let done = 0, skip = 0;
  STUDENTS.forEach(function (s) {
    const sub = emailById[String(s[1]).toLowerCase()];
    if (!sub) { skip++; return; }
    Classroom.Courses.CourseWork.StudentSubmissions.patch(
      { assignedGrade: s[2], draftGrade: s[2] },
      CONFIG.COURSE_ID, cwId, sub.id, { updateMask: "assignedGrade,draftGrade" });
    if (CONFIG.RETURN_TO_STUDENTS && sub.state !== "RETURNED") {
      try {
        Classroom.Courses.CourseWork.StudentSubmissions.return_(
          {}, CONFIG.COURSE_ID, cwId, sub.id);
      } catch (e) { /* 返却済みへの再実行は Precondition failed になるが無害 */ }
    }
    done++;
  });
  Logger.log("点数反映 " + done + " 件 / スキップ " + skip + " 件（未登録・欠席等）");
}
