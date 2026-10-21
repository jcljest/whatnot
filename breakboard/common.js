// Hybrid break: 5 slots, each a mono color + 2 digits the host assigns. Shared by the dock and the overlay.
const BB = (() => {
  // Same palette as tools/build_assets.py
  const COLORS = {
    W: { name: 'White', dot: '#F4EFD9', ink: '#0F0F0F' },
    U: { name: 'Blue',  dot: '#1E73BE', ink: '#FFFFFF' },
    B: { name: 'Black', dot: '#1C1A1A', ink: '#E8E2D6', ring: '#E8E2D6' },
    R: { name: 'Red',   dot: '#D7262E', ink: '#FFFFFF' },
    G: { name: 'Green', dot: '#1B8A4B', ink: '#FFFFFF' },
  };

  function newState() {
    return { visible: true, slots: Object.keys(COLORS).map(color => ({ color, digits: ['', ''], buyer: '' })) };
  }

  // Older saved states (from the multi-mode version) don't have slot.color; start fresh instead.
  const valid = st => Array.isArray(st?.slots) && st.slots.length === 5 && st.slots.every(s => s.color in COLORS);

  return { COLORS, newState, valid };
})();
