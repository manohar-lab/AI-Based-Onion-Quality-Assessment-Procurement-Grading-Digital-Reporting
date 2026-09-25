import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:onion_quality_frontend/core/config/app_config.dart';

/// Lightweight HTTP client wrapper for the backend API.
class ApiClient {
  final String baseUrl;
  final http.Client _client;

  ApiClient({String? baseUrl, http.Client? client})
      : baseUrl = baseUrl ?? AppConfig.apiBaseUrl,
        _client = client ?? http.Client();

  Future<Map<String, dynamic>> get(String path) async {
    final response = await _client.get(Uri.parse('$baseUrl$path'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    }
    throw Exception('GET $path failed: ${response.statusCode}');
  }

  void dispose() {
    _client.close();
  }
}
