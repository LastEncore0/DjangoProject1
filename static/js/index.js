// async function selectFolder(inputId) {
//     console.log("selectFolder");
//     try {
//         const directoryHandle = await window.showDirectoryPicker(); // ✅ 选择文件夹
//         const folderPath = await getDirectoryPath(directoryHandle); // ✅ 获取完整路径
//         document.getElementById(inputId).value = folderPath; // ✅ 更新输入框
//     } catch (err) {
//         console.log("ユーザーがキャンセルされました");
//     }
// }
//
// //  获取完整文件夹路径
// async function getDirectoryPath(directoryHandle) {
//     const paths = [];
//     let currentHandle = directoryHandle;
//
//     while (currentHandle) {
//         paths.unshift(currentHandle.name);
//         try {
//             currentHandle = await currentHandle.getParent();
//         } catch {
//             break;
//         }
//     }
//     console.log("path:",path);
//     return paths.join("/");
// }
//
//  document.getElementById("folderInput").addEventListener("change", function(event) {
//             let files = event.target.files;
//             if (files.length > 0) {
//                 let folderPath = files[0].webkitRelativePath.split("/")[0];
//                 document.getElementById("output").innerText = "選擇的文件夾: " + folderPath;
//             }
//         });