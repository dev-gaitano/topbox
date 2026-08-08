import "./ColorPalettePicker.css";

interface ColorPalettePickerProps {
  colors: string[];
  onChange: (colors: string[]) => void;
  error?: string;
  minColors?: number;
}

const MAX_COLORS = 5;

function ColorPalettePicker({
  colors,
  onChange,
  error,
  minColors = 5,
}: ColorPalettePickerProps) {
  function handleColorChange(index: number, value: string) {
    const updated = [...colors];
    updated[index] = value;
    onChange(updated);
  }

  function addColor() {
    if (colors.length < MAX_COLORS) {
      onChange([...colors, "#000000"]);
    }
  }

  function removeColor(index: number) {
    onChange(colors.filter((_, i) => i !== index));
  }

  return (
    <div className="cpp-wrapper">
      <div className="cpp-swatches">
        {colors.map((color, i) => (
          <div key={i} className="cpp-swatch-item">
            <div className="cpp-swatch" style={{ backgroundColor: color }}>
              <input
                type="color"
                className="cpp-color-input"
                value={color}
                onChange={(e) => handleColorChange(i, e.target.value)}
                title={color}
              />
            </div>
            <input
              type="text"
              className="cpp-hex-input"
              value={color}
              maxLength={7}
              spellCheck={false}
              onChange={(e) => {
                const val = e.target.value;
                // Allow typing freely; only commit valid hex
                if (/^#[0-9A-Fa-f]{6}$/.test(val)) {
                  handleColorChange(i, val);
                } else {
                  // Optimistically show what user is typing via direct DOM update
                  const updated = [...colors];
                  updated[i] = val;
                  onChange(updated);
                }
              }}
              onBlur={(e) => {
                // Reset to last valid hex on blur if invalid
                if (!/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) {
                  handleColorChange(i, color);
                }
              }}
            />
            <button
              type="button"
              className="cpp-remove-btn"
              onClick={() => removeColor(i)}
              aria-label="Remove color"
            >
              ×
            </button>
          </div>
        ))}

        {colors.length < MAX_COLORS && (
          <button type="button" className="cpp-add-btn" onClick={addColor}>
            <span>+</span>
          </button>
        )}
      </div>

      <p className="cpp-hint">
        {colors.length} / {MAX_COLORS}
        {colors.length < minColors && (
          <span className="cpp-hint--warn">
            {" "}
            · Pick at {minColors} brand colors
          </span>
        )}
      </p>

      {error && <p className="cpp-error">{error}</p>}
    </div>
  );
}

export default ColorPalettePicker;
