function clone(value) {
  return structuredClone(value);
}

function stableSerialise(value) {
  if (Array.isArray(value)) {
    return `[${value.map(stableSerialise).join(",")}]`;
  }

  if (value && typeof value === "object") {
    const entries = Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableSerialise(value[key])}`);
    return `{${entries.join(",")}}`;
  }

  return JSON.stringify(value);
}

export function createStateStore(initialScene, maximumHistory = 100) {
  let present = clone(initialScene);
  let past = [];
  let future = [];
  const listeners = new Set();

  function notify() {
    const snapshot = clone(present);
    listeners.forEach((listener) => listener(snapshot));
  }

  function commit(nextScene) {
    const next = clone(nextScene);
    if (stableSerialise(next) === stableSerialise(present)) {
      return false;
    }

    past.push(clone(present));
    if (past.length > maximumHistory) {
      past = past.slice(past.length - maximumHistory);
    }
    present = next;
    future = [];
    notify();
    return true;
  }

  return {
    getScene() {
      return clone(present);
    },

    getHistoryStatus() {
      return {
        canUndo: past.length > 0,
        canRedo: future.length > 0,
        undoDepth: past.length,
        redoDepth: future.length,
      };
    },

    commit,

    update(mutator) {
      const draft = clone(present);
      mutator(draft);
      return commit(draft);
    },

    undo() {
      if (past.length === 0) {
        return false;
      }
      future.unshift(clone(present));
      present = past.pop();
      notify();
      return true;
    },

    redo() {
      if (future.length === 0) {
        return false;
      }
      past.push(clone(present));
      present = future.shift();
      notify();
      return true;
    },

    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },

    serialise() {
      return stableSerialise(present);
    },
  };
}

export { stableSerialise };
