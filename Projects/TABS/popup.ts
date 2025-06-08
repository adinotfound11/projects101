document.getElementById("groupNow")?.addEventListener("click", async () => {
  try {
    await chrome.runtime.sendMessage({ action: "groupTabs" });
  } catch (error) {
    console.error("Error sending message to background:", error);
  }
});