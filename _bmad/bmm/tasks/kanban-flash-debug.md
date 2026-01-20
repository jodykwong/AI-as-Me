# Kanban Flash Debug

## Task
Debug Kanban task card "flash and disappear" issue

## Steps
1. **Confirm**: Record trigger, timing, final state
2. **Console**: Check status logs, errors, render calls
3. **Network**: Monitor API calls (status update, board refresh, execution)
4. **Root Causes**:
   - Auto-refresh (2s) overwriting UI
   - Status jump (Doing→Done instantly)
   - WebSocket race condition
   - CSS animation timing
5. **Locate**: Find `renderBoard`, status handlers, `setInterval` in kanban.js
6. **Fix**: Add timestamps, breakpoints, delay test

## Output
Root cause + fix location
