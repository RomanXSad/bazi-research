import 'package:flutter/material.dart';
import 'name_data.dart';

void main() {
  runApp(const NameApp());
}

class NameApp extends StatelessWidget {
  const NameApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chinese Name Converter',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF8D6E2A),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        fontFamily: 'SF Pro Display',
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _controller = TextEditingController();
  List<NameChar>? _results;
  String? _pinyin;

  final _demoNames = [
    '张伟明', '李慧琳', '王强', '陈雅婷', '刘志强',
    '杨晓慧', '赵睿博', '黄丽娜', '周文杰', '吴秀英'
  ];
  int _demoIdx = 0;
  bool _demoRunning = false;

  void _analyze() {
    final input = _controller.text.trim();
    if (input.isEmpty) {
      setState(() { _results = null; _pinyin = null; });
      return;
    }
    final chars = input.split('');
    final results = <NameChar>[];
    for (final c in chars) {
      results.add(nameDict[c] ?? NameChar(c, '', [], '', '', ''));
    }
    final syllables = results.map((r) => r.pinyin).join(' ');
    setState(() {
      _results = results;
      _pinyin = syllables;
    });
  }

  void _startDemo() {
    setState(() => _demoRunning = true);
    _showDemoName(0);
  }

  void _stopDemo() {
    setState(() => _demoRunning = false);
  }

  void _showDemoName(int idx) {
    if (idx >= _demoNames.length) {
      _stopDemo();
      return;
    }
    _controller.text = _demoNames[idx];
    _demoIdx = idx;
    _analyze();
    Future.delayed(const Duration(seconds: 3), () {
      if (_demoRunning) _showDemoName(idx + 1);
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Color _elementColor(String e) {
    switch (e) {
      case '木': return const Color(0xFF4CAF50);
      case '火': return const Color(0xFFFF5722);
      case '土': return const Color(0xFFFF9800);
      case '金': return const Color(0xFF78909C);
      case '水': return const Color(0xFF2196F3);
      default: return Colors.grey;
    }
  }

  String _elementEmoji(String e) {
    switch (e) {
      case '木': return '🌳';
      case '火': return '🔥';
      case '土': return '⛰️';
      case '金': return '⚙️';
      case '水': return '💧';
      default: return '❓';
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('🀄 Name Converter', style: TextStyle(fontWeight: FontWeight.w700)),
        centerTitle: true,
        actions: [
          IconButton(
            icon: Icon(_demoRunning ? Icons.stop_circle_outlined : Icons.play_circle_outline),
            onPressed: _demoRunning ? _stopDemo : _startDemo,
            tooltip: 'Demo',
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Input
          TextField(
            controller: _controller,
            decoration: InputDecoration(
              hintText: 'Enter Chinese characters...',
              prefixIcon: const Icon(Icons.edit),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              filled: true,
              fillColor: t.colorScheme.surfaceContainerLowest,
              suffixIcon: IconButton(
                icon: const Icon(Icons.search),
                onPressed: _analyze,
              ),
            ),
            textInputAction: TextInputAction.search,
            onSubmitted: (_) => _analyze(),
            style: const TextStyle(fontSize: 20),
          ),
          const SizedBox(height: 8),

          if (_demoRunning)
            Center(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.orange.shade50,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  'Demo ${_demoIdx + 1}/${_demoNames.length}',
                  style: TextStyle(fontSize: 12, color: Colors.orange.shade800),
                ),
              ),
            ),
          const SizedBox(height: 12),

          // Results
          if (_results != null) ...[
            // Pinyin
            if (_pinyin != null && _pinyin!.isNotEmpty)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      Text(_controller.text,
                          style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Text(_pinyin!,
                          style: TextStyle(fontSize: 16, color: Colors.grey.shade600)),
                    ],
                  ),
                ),
              ),

            // Character cards
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: _results!.map((r) {
                  final hasData = r.element.isNotEmpty;
                  return Container(
                    width: 110,
                    margin: const EdgeInsets.only(right: 8),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: t.colorScheme.surfaceContainerLow,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.grey.shade200),
                    ),
                    child: Column(
                      children: [
                        Text(r.char, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 4),
                        if (r.pinyin.isNotEmpty)
                          Text(r.pinyin, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                        if (hasData) ...[
                          const SizedBox(height: 4),
                          Text(r.meanings.take(2).join(' · '),
                              style: const TextStyle(fontSize: 10), textAlign: TextAlign.center),
                          const SizedBox(height: 4),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: _elementColor(r.element),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text('${_elementEmoji(r.element)} ${r.element}',
                                style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w600)),
                          ),
                        ],
                      ],
                    ),
                  );
                }).toList(),
              ),
            ),

            const SizedBox(height: 12),

            // Element distribution
            _ElementBar(results: _results!),

            const SizedBox(height: 12),

            // English name
            _EnglishNameCard(results: _results!),
          ],
        ],
      ),
    );
  }
}

class _ElementBar extends StatelessWidget {
  final List<NameChar> results;
  const _ElementBar({required this.results});

  @override
  Widget build(BuildContext context) {
    final counts = <String, int>{};
    for (final r in results) {
      if (r.element.isNotEmpty) {
        counts[r.element] = (counts[r.element] ?? 0) + 1;
      }
    }
    if (counts.isEmpty) return const SizedBox.shrink();

    final colors = {
      '木': const Color(0xFF4CAF50),
      '火': const Color(0xFFFF5722),
      '土': const Color(0xFFFF9800),
      '金': const Color(0xFF78909C),
      '水': const Color(0xFF2196F3),
    };

    final order = ['木', '火', '土', '金', '水'];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('⚖️ Element Balance', style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: SizedBox(
                height: 8,
                child: Row(
                  children: order.where((e) => counts.containsKey(e)).map((e) {
                    return Expanded(
                      flex: counts[e]!,
                      child: Container(color: colors[e]),
                    );
                  }).toList(),
                ),
              ),
            ),
            const SizedBox(height: 6),
            Wrap(
              spacing: 12,
              runSpacing: 4,
              children: order.where((e) => counts.containsKey(e)).map((e) {
                return Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(width: 8, height: 8, decoration: BoxDecoration(color: colors[e], borderRadius: BorderRadius.circular(2))),
                    const SizedBox(width: 4),
                    Text('$e ${counts[e]}', style: const TextStyle(fontSize: 12)),
                  ],
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}

class _EnglishNameCard extends StatelessWidget {
  final List<NameChar> results;
  const _EnglishNameCard({required this.results});

  String _getEnglishName() {
    if (results.isEmpty) return '';
    final given = results.length > 1 ? results.sublist(1) : results;

    // Try first given name character
    for (final r in given) {
      if (enNames.containsKey(r.char)) {
        final sn = surnames[results[0].char] ?? _capitalize(results[0].pinyin);
        return '${enNames[r.char]!.first} $sn';
      }
    }
    // Fallback
    final sn = surnames[results[0].char] ?? _capitalize(results[0].pinyin);
    return sn;
  }

  String _capitalize(String s) {
    if (s.isEmpty) return '';
    return s[0].toUpperCase() + s.substring(1);
  }

  @override
  Widget build(BuildContext context) {
    final en = _getEnglishName();
    if (en.isEmpty) return const SizedBox.shrink();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text('🌍 English Name', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
            const SizedBox(height: 8),
            Text(en, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text('Based on character meanings', style: TextStyle(fontSize: 11, color: Colors.grey.shade500)),
          ],
        ),
      ),
    );
  }
}
