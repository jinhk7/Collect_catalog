// Scriptable: 夸克网盘播放器脚本
// 需求：扫码登录获取 cookie，访问网盘 API，播放音频文件

// 1. 生成二维码供夸克 App 扫码
// 2. 获取 cookie 并存储
// 3. 获取文件列表
// 4. 播放音频文件

// Scriptable API 文档：https://docs.scriptable.app/

// --- 配置区 ---
const API_BASE = 'https://open.quark.cn/api/v1';
const COOKIE_KEY = 'quark_cookie';

// --- 工具函数 ---
function saveCookie(cookie) {
  Keychain.set(COOKIE_KEY, cookie);
}

function getCookie() {
  return Keychain.get(COOKIE_KEY);
}

function clearCookie() {
  Keychain.remove(COOKIE_KEY);
}

// --- 1. 生成二维码供扫码登录 ---
async function showLoginQRCode() {
  // 假设后端已提供二维码内容（如 ticket 或 URL），此处仅演示二维码生成
  const loginUrl = 'https://open.quark.cn/app/scan-login'; // 实际应由后端生成
  const qr = await generateQRCode(loginUrl);
  const alert = new Alert();
  alert.title = '扫码登录夸克网盘';
  alert.message = '请用夸克App扫码下方二维码登录';
  alert.addImage(qr);
  await alert.present();
  // 登录后需手动输入 cookie
}

async function generateQRCode(text) {
  const req = new Request(`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(text)}`);
  return await req.loadImage();
}

// --- 2. 手动输入 cookie 并存储 ---
async function inputCookie() {
  const alert = new Alert();
  alert.title = '输入夸克网盘Cookie';
  alert.message = '请在扫码登录后，复制浏览器中的Cookie并粘贴到此处';
  alert.addTextField('Cookie', '');
  alert.addAction('保存');
  alert.addCancelAction('取消');
  const idx = await alert.present();
  if (idx === 0) {
    const cookie = alert.textFieldValue(0);
    saveCookie(cookie);
    return cookie;
  }
  return null;
}

// --- 3. 获取文件列表 ---
async function fetchFiles(parentId = '0') {
  const cookie = getCookie();
  if (!cookie) throw new Error('请先扫码登录并输入Cookie');
  const req = new Request(`${API_BASE}/files?parent_id=${parentId}`);
  req.headers = { 'Cookie': cookie };
  const res = await req.loadJSON();
  return res.files || [];
}

// --- 4. 播放音频文件 ---
async function playAudio(url) {
  Safari.open(url);
}

// --- 主流程 ---
async function main() {
  let cookie = getCookie();
  if (!cookie) {
    await showLoginQRCode();
    cookie = await inputCookie();
    if (!cookie) return;
  }
  // 获取文件列表
  let files = [];
  try {
    files = await fetchFiles();
  } catch (e) {
    clearCookie();
    console.error(e);
    return;
  }
  // 展示文件列表
  const alert = new Alert();
  alert.title = '选择音频文件';
  files.filter(f => f.type === 'file').forEach(f => alert.addAction(f.name));
  alert.addCancelAction('退出');
  const idx = await alert.present();
  if (idx < files.length) {
    const file = files[idx];
    // 获取下载链接（假设API返回download_url字段）
    const url = file.download_url || file.url;
    await playAudio(url);
  }
}

main();
