import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the neonex-theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'neonex-theme:plugin',
  description: 'A Neonex Theme for Jupyter Lab',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension neonex-theme is activated!');
    const style = 'neonex-theme/index.css';

    manager.register({
      name: 'neonex-theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
