"use strict";
function getDomain(url) {
    try {
        const { hostname } = new URL(url);
        return hostname.replace(/^www\./, '');
    }
    catch {
        return 'unknown';
    }
}
async function autoGroupTabsByDomain() {
    const tabs = await chrome.tabs.query({ currentWindow: true });
    // Explicitly define the type for domainGroups
    const domainGroups = {};
    for (const tab of tabs) {
        if (!tab.url || typeof tab.id !== 'number')
            continue;
        const domain = getDomain(tab.url);
        if (!domainGroups[domain]) {
            domainGroups[domain] = [];
        }
        domainGroups[domain].push(tab.id);
    }
    for (const [domain, tabIds] of Object.entries(domainGroups)) {
        if (tabIds.length < 2)
            continue;
        const groupId = await chrome.tabs.group({ tabIds });
        await chrome.tabGroups.update(groupId, {
            title: domain,
            color: "green"
        });
    }
}
// Automatically group when the extension is installed or the browser starts
chrome.runtime.onInstalled.addListener(() => {
    autoGroupTabsByDomain().catch(console.error);
});
chrome.runtime.onStartup.addListener(() => {
    autoGroupTabsByDomain().catch(console.error);
});
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message.action === "groupTabs") {
        autoGroupTabsByDomain().then(() => sendResponse({ status: "done" })).catch(console.error);
        return true; // Keep the message channel open for async sendResponse
    }
});
