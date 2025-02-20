import React, { useState } from 'react';
import {
    PieChartOutlined,
    DollarOutlined,
    FileTextOutlined,
    AppstoreOutlined,
    BarChartOutlined
} from '@ant-design/icons';
import { Layout, Menu, theme } from 'antd';

const { Header, Content, Sider } = Layout;

// Конфигурация меню с контентом
const menuConfig = [
    {
        key: 'finance',
        label: 'Финансы',
        sideMenu: [
            {
                key: 'transactions',
                icon: <DollarOutlined />,
                label: 'Транзакции',
                content: <div className="p-4">Список транзакций...</div>
            },
            {
                key: 'categories',
                icon: <AppstoreOutlined />,
                label: 'Категории',
                content: <div className="p-4">Управление категориями...</div>
            },
        ],
    },
    {
        key: 'reports',
        label: 'Отчёты',
        sideMenu: [
            {
                key: 'monthly',
                icon: <PieChartOutlined />,
                label: 'Месячный отчёт',
                content: <div className="p-4">Графики за месяц...</div>
            },
            {
                key: 'annual',
                icon: <BarChartOutlined />,
                label: 'Годовой отчёт',
                content: <div className="p-4">Годовые статистика...</div>
            },
        ],
    },
];

const App = () => {
    const [selectedMainMenu, setSelectedMainMenu] = useState('finance');
    const [selectedSubMenu, setSelectedSubMenu] = useState('transactions');
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    const handleMainMenuSelect = ({ key }) => {
        setSelectedMainMenu(key);
        // Автоматически выбираем первый пункт подменю
        const firstSubItem = menuConfig.find(m => m.key === key)?.sideMenu[0]?.key;
        setSelectedSubMenu(firstSubItem);
    };

    const handleSideMenuSelect = ({ key }) => {
        setSelectedSubMenu(key);
    };

    // Получаем текущие пункты сайдбара
    const currentSideMenu = menuConfig.find(
        item => item.key === selectedMainMenu
    )?.sideMenu || [];

    // Получаем текущий контент
    const currentContent = currentSideMenu.find(
        item => item.key === selectedSubMenu
    )?.content || <div>Выберите раздел</div>;

    return (
        <Layout>
            <Header style={{ display: 'flex', alignItems: 'center' }}>
                <div className="font-bold text-3xl text-orange-500 mr-8">
                    FinanceTracker
                </div>
                <Menu
                    theme="dark"
                    mode="horizontal"
                    selectedKeys={[selectedMainMenu]}
                    onSelect={handleMainMenuSelect}
                    items={menuConfig.map(item => ({
                        key: item.key,
                        label: item.label,
                    }))}
                    style={{ flex: 1 }}
                />
            </Header>

            <Layout>
                <Sider width={200} style={{ background: colorBgContainer }}>
                    <Menu
                        mode="inline"
                        selectedKeys={[selectedSubMenu]}
                        onSelect={handleSideMenuSelect}
                        items={currentSideMenu.map(item => ({
                            key: item.key,
                            icon: item.icon,
                            label: item.label,
                        }))}
                        style={{ height: '100%', borderRight: 0 }}
                    />
                </Sider>

                <Content style={{
                    padding: 24,
                    background: colorBgContainer,
                    minHeight: 'calc(100vh - 64px)'
                }}>
                    <div className="bg-white p-6 rounded-lg shadow">
                        {currentContent}
                    </div>
                </Content>
            </Layout>
        </Layout>
    );
};

export default App;