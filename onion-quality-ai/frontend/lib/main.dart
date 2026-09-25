import 'package:flutter/material.dart';
import 'package:onion_quality_frontend/features/home/home_screen.dart';
import 'package:onion_quality_frontend/core/theme/app_theme.dart';

void main() {
  runApp(const OnionQualityApp());
}

class OnionQualityApp extends StatelessWidget {
  const OnionQualityApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Onion Quality Assessment',
      theme: AppTheme.darkTheme,
      debugShowCheckedModeBanner: false,
      home: const HomeScreen(),
    );
  }
}
