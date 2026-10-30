const fs = require('fs');
const path = require('path');
const readline = require('readline');

const htmlFile = path.join(__dirname, 'スマホ用_50km補給タイムテーブル.html');
if (!fs.existsSync(htmlFile)) {
  console.error('エラー: スマホ用_50km補給タイムテーブル.html が見つかりません。');
  process.exit(1);
}

const html = fs.readFileSync(htmlFile, 'utf8');

function clean(str) {
  return str ? str.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim() : '';
}

function escapeICS(str) {
  return str.replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,');
}

const items = [];
const cardMatches = html.split('<div class="card');
cardMatches.shift();

for (let c of cardMatches) {
  const block = '<div class="card' + c.split('<!-- ')[0];
  const timeM = block.match(/<span class="time">([0-9:]+)<\/span>/);
  if (!timeM) continue;
  const time = timeM[1];

  const distM = block.match(/<span class="dist">([^<]+)<\/span>/);
  const dist = distM ? distM[1].trim() : '';

  const titleM = block.match(/<div class="item-title">([\s\S]*?)<\/div>/);
  const title = titleM ? clean(titleM[1]) : '補給タイム';

  const waterM = block.match(/<div class="water-box"[^>]*>([\s\S]*?)<\/div>/);
  const water = waterM ? clean(waterM[1]) : '';

  const infoM = block.match(/<div class="info-grid">([\s\S]*?)<\/div>/);
  const info = infoM ? clean(infoM[1]) : '';

  const pointM = block.match(/<div class="point">([\s\S]*?)<\/div>/);
  const point = pointM ? clean(pointM[1]) : '';

  items.push({ time, dist, title, water, info, point });
}

function generateICS(dateObj, label, outFilename) {
  const y = dateObj.getFullYear();
  const m = String(dateObj.getMonth() + 1).padStart(2, '0');
  const d = String(dateObj.getDate()).padStart(2, '0');
  const ymd = `${y}${m}${d}`;
  const nowStamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
  const events = [];

  items.forEach((it, idx) => {
    const parts = it.time.split(':');
    const hh = parts[0].padStart(2, '0');
    const mm = parts[1].padStart(2, '0');

    let sH = parseInt(hh, 10);
    let sM = parseInt(mm, 10);
    let eM = sM + 15;
    let eH = sH;
    if (eM >= 60) {
      eM -= 60;
      eH = (eH + 1) % 24;
    }
    const endHh = String(eH).padStart(2, '0');
    const endMm = String(eM).padStart(2, '0');

    const dtStart = `${ymd}T${hh}${mm}00`;
    const dtEnd = `${ymd}T${endHh}${endMm}00`;
    const uid = `${ymd}T${hh}${mm}00-${idx + 1}@3daymarch.50km`;

    const summary = '【補給 ' + it.time + '】' + (it.dist ? '[' + it.dist + '] ' : '') + it.title;

    const descLines = [];
    if (it.dist) descLines.push('■ 区分: ' + it.dist);
    if (it.water) descLines.push('■ ' + it.water);
    if (it.info) descLines.push('■ ' + it.info);
    if (it.point) descLines.push('■ 要点: ' + it.point);
    const description = descLines.map(escapeICS).join('\\n');

    events.push([
      'BEGIN:VEVENT',
      'UID:' + uid,
      'DTSTAMP:' + nowStamp,
      'DTSTART:' + dtStart,
      'DTEND:' + dtEnd,
      'SUMMARY:' + escapeICS(summary),
      'DESCRIPTION:' + description,
      'BEGIN:VALARM',
      'ACTION:DISPLAY',
      'DESCRIPTION:' + escapeICS(summary),
      'TRIGGER:-PT0M',
      'END:VALARM',
      'END:VEVENT'
    ].join('\r\n'));
  });

  const ics = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Japan Three Day March 50km//Supply Timetable//JA',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    events.join('\r\n'),
    'END:VCALENDAR'
  ].join('\r\n');

  fs.writeFileSync(path.join(__dirname, outFilename), ics, 'utf8');
  console.log(`✅ 作成完了: ${outFilename} (${y}/${m}/${d} - ${label})`);
}

function processWithDate(dateStr) {
  const parts = dateStr.trim().split('-');
  if (parts.length !== 3) {
    console.error('❌ 日付の形式が正しくありません。YYYY-MM-DD 形式（例: 2027-11-05）で指定してください。');
    process.exit(1);
  }
  const y = parseInt(parts[0], 10);
  const m = parseInt(parts[1], 10) - 1;
  const d = parseInt(parts[2], 10);

  const day1 = new Date(y, m, d);
  const day2 = new Date(y, m, d + 1);
  const day3 = new Date(y, m, d + 2);

  console.log(`\nタイムテーブルから ${items.length} 件の補給スケジュールを検出しました。`);
  console.log(`指定された大会初日: ${dateStr}\n`);

  generateICS(day1, '1日目', '50km補給_1日目.ics');
  generateICS(day2, '2日目', '50km補給_2日目.ics');
  generateICS(day3, '3日目', '50km補給_3日目.ics');

  // 日付入りファイル名およびテスト用も更新
  const m1 = String(day1.getMonth() + 1);
  const d1 = String(day1.getDate());
  const m2 = String(day2.getMonth() + 1);
  const d2 = String(day2.getDate());
  const m3 = String(day3.getMonth() + 1);
  const d3 = String(day3.getDate());
  generateICS(day1, '1日目', `50km補給_${m1}月${d1}日_1日目.ics`);
  generateICS(day2, '2日目', `50km補給_${m2}月${d2}日_2日目.ics`);
  generateICS(day3, '3日目', `50km補給_${m3}月${d3}日_3日目.ics`);
  generateICS(new Date(), 'テスト用', '50km補給_今日テスト用.ics');

  console.log('\n🎉 全日程（1日目・2日目・3日目）のカレンダーファイルを更新しました！');
  console.log('スマホで「スマホ用_50km補給タイムテーブル.html」を開くか、');
  console.log('生成された .ics ファイルをタップしてカレンダーに追加してください。\n');
}

// 引数がある場合
if (process.argv[2]) {
  processWithDate(process.argv[2]);
} else {
  // 対話入力
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('============================================================');
  console.log('【日本スリーデーマーチ】来年用 Apple Watch 補給アラーム更新');
  console.log('============================================================');
  console.log('来年の大会1日目の日付を YYYY-MM-DD 形式で入力してください。');
  console.log('（例: 2027年11月5日の場合は「2027-11-05」と入力してEnter）\n');

  rl.question('1日目の日付: ', (answer) => {
    rl.close();
    processWithDate(answer);
  });
}

