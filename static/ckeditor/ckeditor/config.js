/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function (config) {
	// Define changes to default configuration here.
	// For the complete reference:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// Comment the following line in DEBUG mode:
	config.removePlugins = 'devtools';
	
	// See the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Make dialogs simpler.
	config.removeDialogTabs = 'image:advanced;image:Link;link:advanced;link:upload';
	config.linkShowTargetTab = false;

	// In CKEditor 4.1 or higher you need to disable ACF (Advanced Content Filter)
	// to make Youtube plugin work:
	config.allowedContent = true;
};

CKEDITOR.on('dialogDefinition', function (ev) {
	// Take the dialog name and its definition from the event data.
	var dialogName = ev.data.name;
	var dialogDefinition = ev.data.definition;

	// Check if the definition is from the dialog we're
	// interested in (the 'link' dialog).
	if (dialogName == 'link') {
		//        Remove the 'Upload' and 'Advanced' tabs from the 'Link' dialog.
		//        dialogDefinition.removeContents('upload');
		//        dialogDefinition.removeContents('advanced');

		// Get a reference to the 'Link Info' tab.
		var infoTab = dialogDefinition.getContents('info');
		// Remove unnecessary widgets from the 'Link Info' tab.
		infoTab.remove('linkType');
		infoTab.remove('protocol');
		infoTab.remove('browse');

		// Get a reference to the "Target" tab and set default to '_blank'
		var targetTab = dialogDefinition.getContents('target');
		var targetField = targetTab.get('linkTargetType');
		targetField['default'] = '_blank';

	} else if (dialogName == 'image') {
		//        Remove the 'Link' and 'Advanced' tabs from the 'Image' dialog.
		//        dialogDefinition.removeContents('Link');
		//        dialogDefinition.removeContents('advanced');

		// Get a reference to the 'Image Info' tab.
		var infoTab = dialogDefinition.getContents('info');
		// Remove unnecessary widgets/elements from the 'Image Info' tab.
		infoTab.remove('browse');
		infoTab.remove('txtHSpace');
		infoTab.remove('txtVSpace');
		infoTab.remove('txtBorder');
		// infoTab.remove('cmbAlign');

	}
});
