async function selectFolder(inputId) {
    try {
        const directoryHandle = await window.showDirectoryPicker(); // ✅ 选择文件夹
        const folderPath = await getDirectoryPath(directoryHandle); // ✅ 获取完整路径
        document.getElementById(inputId).value = folderPath; // ✅ 更新输入框
    } catch (err) {
        console.log("ユーザーがキャンセルされました");
    }
}

//  获取完整文件夹路径
async function getDirectoryPath(directoryHandle) {
    const paths = [];
    let currentHandle = directoryHandle;

    while (currentHandle) {
        paths.unshift(currentHandle.name);
        try {
            currentHandle = await currentHandle.getParent();
        } catch {
            break;
        }
    }

    return paths.join("/");
}
