const plugins = [];
const presets = new Map();
const drawers = new Map();
export class Plugins {
    static getPlugin(plugin) {
        return plugins.find((t) => t.id === plugin);
    }
    static addPlugin(plugin) {
        if (!Plugins.getPlugin(plugin.id)) {
            plugins.push(plugin);
        }
    }
    static getAvailablePlugins(container) {
        const res = new Map();
        for (const plugin of plugins) {
            if (!plugin.needsPlugin(container.options)) {
                continue;
            }
            res.set(plugin.id, plugin.getPlugin(container));
        }
        return res;
    }
    static loadOptions(options, sourceOptions) {
        for (const plugin of plugins) {
            plugin.loadOptions(options, sourceOptions);
        }
    }
    static getPreset(preset) {
        return presets.get(preset);
    }
    static addPreset(presetKey, options) {
        if (!Plugins.getPreset(presetKey)) {
            presets.set(presetKey, options);
        }
    }
    static addShapeDrawer(type, drawer) {
        if (!Plugins.getShapeDrawer(type)) {
            drawers.set(type, drawer);
        }
    }
    static getShapeDrawer(type) {
        return drawers.get(type);
    }
    static getSupportedShapes() {
        return drawers.keys();
    }
}
