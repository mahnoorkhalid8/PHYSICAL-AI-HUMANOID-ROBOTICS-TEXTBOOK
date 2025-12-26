import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI Humanoid Robotics Guide',
  tagline: 'A comprehensive guide to building intelligent humanoid robots',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://physical-ai-humanoid-robotics-textbook.vercel.app', // Replace with your Vercel URL
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/', // For Vercel deployment

  // For development proxy to backend
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'mahnoorkhalid8', // Your GitHub username or organization name.
  projectName: 'my-physical-ai-humanoid-textbook', // Your repository name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Add client modules to inject the chatbot on all pages
  clientModules: [
    require.resolve('./src/utils/injectChatbot.js'),
    require.resolve('./src/components/Root.tsx'),
  ],


  plugins: [
    // Add development server proxy configuration
    async function myPlugin() {
      return {
        name: 'custom-webpack-config',
        configureWebpack(config, isServer, utils) {
          return {
            devServer: {
              proxy: [
                {
                  context: ['/api'],
                  target: 'http://localhost:8000',
                  changeOrigin: true,
                  secure: false,
                }
              ],
            },
          };
        },
      };
    },
  ],


  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/mahnoorkhalid8/PHYSICAL-AI-HUMANOID-ROBOTICS-TEXTBOOK/tree/main/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical-AI-Humanoid-Robotics-Textbook',
      logo: {
        alt: 'Physical AI Humanoid Robotics Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/mahnoorkhalid8/PHYSICAL-AI-HUMANOID-ROBOTICS-TEXTBOOK',
          label: 'GitHub',
          position: 'right',
        },
        {to: '/sign-in', label: 'Sign In', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Book',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'X',
              href: 'https://x.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/mahnoorkhalid8/Physical-AI-Humanoid-Robotics-Textbook',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Humanoid Robotics Textbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
  // Configuration for production deployment
  // In production, API calls will go directly to the backend server
  // The vercel.json file handles proxying for the deployed version
};

export default config;
