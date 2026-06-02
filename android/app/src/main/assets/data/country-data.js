// 留学目的地数据库 — 所有国家配置
const COUNTRIES = [
  {
    id: 'usa',
    name: '美国',
    flag: '🇺🇸',
    continent: '北美洲',
    currency: { code: 'USD', name: '美元', symbol: '$', rate: 7.2 },
    timezone: { zone: 'America/New_York', utc: 'UTC-5/-4', city: '纽约' },
    languages: [{ code: 'en', name: '英语' }],
    cost: { city: '纽约', monthly: '10000-15000元', tuition: '20-50万/年' }
  },
  {
    id: 'uk',
    name: '英国',
    flag: '🇬🇧',
    continent: '欧洲',
    currency: { code: 'GBP', name: '英镑', symbol: '£', rate: 9.1 },
    timezone: { zone: 'Europe/London', utc: 'UTC+0/+1', city: '伦敦' },
    languages: [{ code: 'en', name: '英语' }],
    cost: { city: '伦敦', monthly: '8000-12000元', tuition: '15-35万/年' }
  },
  {
    id: 'australia',
    name: '澳大利亚',
    flag: '🇦🇺',
    continent: '大洋洲',
    currency: { code: 'AUD', name: '澳元', symbol: 'A$', rate: 4.7 },
    timezone: { zone: 'Australia/Sydney', utc: 'UTC+10/+11', city: '悉尼' },
    languages: [{ code: 'en', name: '英语' }],
    cost: { city: '悉尼', monthly: '8000-12000元', tuition: '15-30万/年' }
  },
  {
    id: 'canada',
    name: '加拿大',
    flag: '🇨🇦',
    continent: '北美洲',
    currency: { code: 'CAD', name: '加元', symbol: 'C$', rate: 5.3 },
    timezone: { zone: 'America/Toronto', utc: 'UTC-5/-4', city: '多伦多' },
    languages: [{ code: 'en', name: '英语' }, { code: 'fr', name: '法语' }],
    cost: { city: '多伦多', monthly: '7000-10000元', tuition: '10-25万/年' }
  },
  {
    id: 'japan',
    name: '日本',
    flag: '🇯🇵',
    continent: '亚洲',
    currency: { code: 'JPY', name: '日元', symbol: '¥', rate: 0.048 },
    timezone: { zone: 'Asia/Tokyo', utc: 'UTC+9', city: '东京' },
    languages: [{ code: 'ja', name: '日语' }],
    cost: { city: '东京', monthly: '6000-9000元', tuition: '5-15万/年' }
  },
  {
    id: 'korea',
    name: '韩国',
    flag: '🇰🇷',
    continent: '亚洲',
    currency: { code: 'KRW', name: '韩元', symbol: '₩', rate: 0.0054 },
    timezone: { zone: 'Asia/Seoul', utc: 'UTC+9', city: '首尔' },
    languages: [{ code: 'ko', name: '韩语' }],
    cost: { city: '首尔', monthly: '5000-8000元', tuition: '4-12万/年' }
  },
  {
    id: 'germany',
    name: '德国',
    flag: '🇩🇪',
    continent: '欧洲',
    currency: { code: 'EUR', name: '欧元', symbol: '€', rate: 7.8 },
    timezone: { zone: 'Europe/Berlin', utc: 'UTC+1/+2', city: '柏林' },
    languages: [{ code: 'de', name: '德语' }],
    cost: { city: '柏林', monthly: '5000-8000元', tuition: '0-3万/年（公立免学费）' }
  },
  {
    id: 'france',
    name: '法国',
    flag: '🇫🇷',
    continent: '欧洲',
    currency: { code: 'EUR', name: '欧元', symbol: '€', rate: 7.8 },
    timezone: { zone: 'Europe/Paris', utc: 'UTC+1/+2', city: '巴黎' },
    languages: [{ code: 'fr', name: '法语' }],
    cost: { city: '巴黎', monthly: '6000-9000元', tuition: '0-5万/年（公立）' }
  },
  {
    id: 'russia',
    name: '俄罗斯',
    flag: '🇷🇺',
    continent: '欧洲/亚洲',
    currency: { code: 'RUB', name: '卢布', symbol: '₽', rate: 0.078 },
    timezone: { zone: 'Europe/Moscow', utc: 'UTC+3', city: '莫斯科' },
    languages: [{ code: 'ru', name: '俄语' }],
    cost: { city: '莫斯科', monthly: '3000-5000元', tuition: '2-8万/年' }
  },
  {
    id: 'kazakhstan',
    name: '哈萨克斯坦',
    flag: '🇰🇿',
    continent: '亚洲',
    currency: { code: 'KZT', name: '坚戈', symbol: '₸', rate: 0.014 },
    timezone: { zone: 'Asia/Almaty', utc: 'UTC+5', city: '阿拉木图' },
    languages: [{ code: 'ru', name: '俄语' }, { code: 'kk', name: '哈语' }],
    cost: { city: '阿拉木图', monthly: '2000-4000元', tuition: '1-5万/年' }
  },
  {
    id: 'azerbaijan',
    name: '阿塞拜疆',
    flag: '🇦🇿',
    continent: '亚洲',
    currency: { code: 'AZN', name: '马纳特', symbol: '₼', rate: 4.2 },
    timezone: { zone: 'Asia/Baku', utc: 'UTC+4', city: '巴库' },
    languages: [{ code: 'az', name: '阿塞拜疆语' }, { code: 'ru', name: '俄语' }],
    cost: { city: '巴库', monthly: '2000-4000元', tuition: '1-4万/年' }
  },
  {
    id: 'malaysia',
    name: '马来西亚',
    flag: '🇲🇾',
    continent: '亚洲',
    currency: { code: 'MYR', name: '林吉特', symbol: 'RM', rate: 1.55 },
    timezone: { zone: 'Asia/Kuala_Lumpur', utc: 'UTC+8', city: '吉隆坡' },
    languages: [{ code: 'ms', name: '马来语' }, { code: 'en', name: '英语' }],
    cost: { city: '吉隆坡', monthly: '2500-4000元', tuition: '3-11万/年' }
  },
  {
    id: 'singapore',
    name: '新加坡',
    flag: '🇸🇬',
    continent: '亚洲',
    currency: { code: 'SGD', name: '新加坡元', symbol: 'S$', rate: 5.3 },
    timezone: { zone: 'Asia/Singapore', utc: 'UTC+8', city: '新加坡' },
    languages: [{ code: 'en', name: '英语' }, { code: 'zh', name: '中文' }],
    cost: { city: '新加坡', monthly: '5000-8000元', tuition: '8-20万/年' }
  }
];

// 获取国家配置
function getCountry(id) {
  return COUNTRIES.find(c => c.id === id) || COUNTRIES.find(c => c.id === 'kazakhstan');
}

// 保存/读取用户选择
function getSelectedCountry() {
  const id = localStorage.getItem('selected_country');
  return getCountry(id);
}

function setSelectedCountry(id) {
  localStorage.setItem('selected_country', id);
}
