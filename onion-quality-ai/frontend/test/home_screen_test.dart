import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onion_quality_frontend/features/home/home_screen.dart';

void main() {
  testWidgets('HomeScreen displays app title', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: HomeScreen()),
    );

    expect(find.text('Onion Quality Assessment'), findsOneWidget);
  });

  testWidgets('HomeScreen has three feature buttons', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: HomeScreen()),
    );

    expect(find.text('Start Inspection'), findsOneWidget);
    expect(find.text('View Results'), findsOneWidget);
    expect(find.text('Reports'), findsOneWidget);
  });

  testWidgets('Feature button tap shows snackbar', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: HomeScreen()),
    );

    await tester.tap(find.text('Start Inspection'));
    await tester.pumpAndSettle();

    expect(find.text('Inspection — Not implemented yet'), findsOneWidget);
  });
}
