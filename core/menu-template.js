const { ipcMain } = require('electron');
const os = require('os');
const { BrowserWindow } = require('electron');
const { version } = require('../../package.json');
const aboutBruno = require('./about-bruno');

const template = [
  {
    label: '集合 (Collection)',
    submenu: [
      {
        label: '打开集合 (Open Collection)',
        click() {
          ipcMain.emit('menu:open-collection');
        }
      },
      {
        label: '最近打开 (Open Recent)',
        role: 'recentdocuments',
        visible: os.platform() == 'darwin',
        submenu: [
          {
            label: '清除最近记录',
            role: 'clearrecentdocuments'
          }
        ]
      },
      { type: 'separator' },
      {
        label: '退出 (Quit)',
        click() {
          ipcMain.emit('main:start-quit-flow');
        }
      },
      {
        label: '强制退出 (Force Quit)',
        click() {
          process.exit();
        }
      }
    ]
  },
  {
    label: '编辑 (Edit)',
    submenu: [
      { role: 'undo', label: '撤销' },
      { role: 'redo', label: '重做' },
      { type: 'separator' },
      { role: 'cut', label: '剪切' },
      { role: 'copy', label: '复制' },
      { role: 'paste', label: '粘贴' },
      { role: 'selectAll', label: '全选' },
      { type: 'separator' },
      { role: 'hide', label: '隐藏' },
      { role: 'hideOthers', label: '隐藏其他' }
    ]
  },
  {
    label: '视图 (View)',
    submenu: [
      { role: 'toggledevtools', label: '切换开发者工具' },
      { type: 'separator' },
      {
        label: '实际大小 (Actual Size)',
        accelerator: 'CommandOrControl+0',
        registerAccelerator: false,
        click() {
          ipcMain.emit('menu:reset-zoom');
        }
      },
      {
        label: '放大 (Zoom In)',
        accelerator: 'CommandOrControl+Plus',
        registerAccelerator: false,
        click() {
          ipcMain.emit('menu:zoom-in');
        }
      },
      {
        label: '缩小 (Zoom Out)',
        accelerator: 'CommandOrControl+-',
        registerAccelerator: false,
        click() {
          ipcMain.emit('menu:zoom-out');
        }
      },
      { type: 'separator' },
      { role: 'togglefullscreen', label: '切换全屏' }
    ]
  },
  {
    role: 'window',
    label: '窗口 (Window)',
    submenu: [
      { role: 'minimize', label: '最小化' },
      { role: 'close', label: '关闭', accelerator: 'CommandOrControl+Shift+Q' }
    ]
  },
  {
    role: 'help',
    label: '帮助 (Help)',
    submenu: [
      {
        label: '关于 Bruno (About Bruno)',
        click: () => {
          const aboutWindow = new BrowserWindow({
            width: 350,
            height: 250,
            maxWidth: 350,
            maxHeight: 250,
            resizable: false,
            fullscreenable: false,
            modal: true
          });
          aboutWindow.setBounds({
            width: 350,
            height: 250
          });
          aboutWindow.center();
          aboutWindow.removeMenu();
          aboutWindow.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(aboutBruno({ version }))}`);
        }
      },
      { label: '官方文档 (Documentation)', click: () => ipcMain.emit('main:open-docs') }
    ]
  }
];

module.exports = template;
