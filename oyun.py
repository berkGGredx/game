import React, { useState, useEffect, useCallback } from 'react';
import { Coins, Zap, TrendingUp } from 'lucide-react';

export default function TapToEarnGame() {
  const [coins, setCoins] = useState(0);
  const [energy, setEnergy] = useState(1000);
  const [maxEnergy, setMaxEnergy] = useState(1000);
  const [coinsPerTap, setCoinsPerTap] = useState(1);
  const [energyRegenRate, setEnergyRegenRate] = useState(1);
  const [level, setLevel] = useState(1);
  const [activeTab, setActiveTab] = useState('game');
  const [clickEffects, setClickEffects] = useState([]);
  const [dailyStreak, setDailyStreak] = useState(1);

  // Enerji yenileme
  useEffect(() => {
    const interval = setInterval(() => {
      setEnergy(prev => Math.min(prev + energyRegenRate, maxEnergy));
    }, 1000);
    return () => clearInterval(interval);
  }, [energyRegenRate, maxEnergy]);

  // Seviye hesaplama
  useEffect(() => {
    const newLevel = Math.floor(coins / 1000) + 1;
    setLevel(newLevel);
  }, [coins]);

  // Tıklama efekti
  const handleTap = useCallback((e) => {
    if (energy >= 1) {
      const rect = e.currentTarget.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      setCoins(prev => prev + coinsPerTap);
      setEnergy(prev => prev - 1);
      
      // Görsel efekt ekle
      const id = Date.now();
      setClickEffects(prev => [...prev, { id, x, y, amount: coinsPerTap }]);
      setTimeout(() => {
        setClickEffects(prev => prev.filter(effect => effect.id !== id));
      }, 1000);
    }
  }, [energy, coinsPerTap]);

  // Yükseltmeler
  const upgrades = [
    {
      id: 'tap',
      name: 'Tıklama Gücü',
      icon: Coins,
      description: 'Her tıklamada daha fazla coin kazan',
      cost: Math.floor(100 * Math.pow(1.5, coinsPerTap)),
      level: coinsPerTap,
      onUpgrade: () => setCoinsPerTap(prev => prev + 1)
    },
    {
      id: 'energy',
      name: 'Maksimum Enerji',
      icon: Zap,
      description: 'Enerji kapasiteni artır',
      cost: Math.floor(200 * Math.pow(1.5, maxEnergy / 1000)),
      level: maxEnergy / 1000,
      onUpgrade: () => setMaxEnergy(prev => prev + 1000)
    },
    {
      id: 'regen',
      name: 'Enerji Yenileme',
      icon: TrendingUp,
      description: 'Enerji yenileme hızını artır',
      cost: Math.floor(300 * Math.pow(1.5, energyRegenRate)),
      level: energyRegenRate,
      onUpgrade: () => setEnergyRegenRate(prev => prev + 1)
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-black text-white rounded-full flex items-center justify-center font-bold">
            {level}
          </div>
          <div>
            <div className="text-xs text-gray-500">Seviye {level}</div>
            <div className="text-sm font-bold text-gray-900">{dailyStreak} gün seri</div>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center gap-2 justify-end">
            <Coins className="w-5 h-5 text-gray-700" />
            <span className="text-2xl font-bold text-gray-900">{coins.toLocaleString()}</span>
          </div>
          <div className="text-xs text-gray-500">Toplam Coin</div>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4 pb-20">
        {activeTab === 'game' && (
          <div className="space-y-4">
            {/* Energy Bar */}
            <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Zap className="w-5 h-5 text-gray-700" />
                  <span className="font-bold text-gray-900">Enerji</span>
                </div>
                <span className="text-sm text-gray-600">{energy} / {maxEnergy}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div 
                  className="bg-gray-900 h-full transition-all duration-300"
                  style={{ width: `${(energy / maxEnergy) * 100}%` }}
                />
              </div>
            </div>

            {/* Tap Area */}
            <div className="relative flex items-center justify-center h-96">
              <button
                onClick={handleTap}
                disabled={energy < 1}
                className="relative w-64 h-64 bg-white border-4 border-gray-900 rounded-full shadow-2xl transform transition-all duration-100 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center hover:shadow-xl"
              >
                <span className="text-6xl font-black text-gray-900">QicX</span>
                {clickEffects.map(effect => (
                  <div
                    key={effect.id}
                    className="absolute text-2xl font-bold text-gray-900 animate-ping"
                    style={{
                      left: effect.x,
                      top: effect.y,
                      animation: 'ping 1s cubic-bezier(0, 0, 0.2, 1)'
                    }}
                  >
                    +{effect.amount}
                  </div>
                ))}
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-white border border-gray-200 rounded-xl p-3 text-center shadow-sm">
                <div className="text-2xl font-bold text-gray-900">+{coinsPerTap}</div>
                <div className="text-xs text-gray-500">Tıklama Başı</div>
              </div>
              <div className="bg-white border border-gray-200 rounded-xl p-3 text-center shadow-sm">
                <div className="text-2xl font-bold text-gray-900">+{energyRegenRate}/s</div>
                <div className="text-xs text-gray-500">Enerji Yenileme</div>
              </div>
              <div className="bg-white border border-gray-200 rounded-xl p-3 text-center shadow-sm">
                <div className="text-2xl font-bold text-gray-900">{level}</div>
                <div className="text-xs text-gray-500">Seviye</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'upgrade' && (
          <div className="space-y-3">
            <h2 className="text-2xl font-bold mb-4 text-gray-900">Yükseltmeler</h2>
            {upgrades.map(upgrade => (
              <div key={upgrade.id} className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gray-900 text-white rounded-xl flex items-center justify-center">
                    <upgrade.icon className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-900">{upgrade.name}</div>
                    <div className="text-sm text-gray-600">{upgrade.description}</div>
                    <div className="text-xs text-gray-500 mt-1">Seviye: {upgrade.level}</div>
                  </div>
                  <button
                    onClick={() => {
                      if (coins >= upgrade.cost) {
                        setCoins(prev => prev - upgrade.cost);
                        upgrade.onUpgrade();
                      }
                    }}
                    disabled={coins < upgrade.cost}
                    className="bg-gray-900 text-white px-4 py-2 rounded-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-800 transition-colors"
                  >
                    <div className="flex items-center gap-1">
                      <Coins className="w-4 h-4" />
                      <span>{upgrade.cost}</span>
                    </div>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg">
        <div className="flex justify-around p-3">
          <button
            onClick={() => setActiveTab('game')}
            className={`flex flex-col items-center gap-1 px-6 py-2 rounded-lg transition-colors ${
              activeTab === 'game' ? 'text-gray-900 bg-gray-100' : 'text-gray-500'
            }`}
          >
            <Coins className="w-6 h-6" />
            <span className="text-xs font-medium">Oyun</span>
          </button>
          <button
            onClick={() => setActiveTab('upgrade')}
            className={`flex flex-col items-center gap-1 px-6 py-2 rounded-lg transition-colors ${
              activeTab === 'upgrade' ? 'text-gray-900 bg-gray-100' : 'text-gray-500'
            }`}
          >
            <TrendingUp className="w-6 h-6" />
            <span className="text-xs font-medium">Yükseltme</span>
          </button>
        </div>
      </div>
    </div>
  );
}
